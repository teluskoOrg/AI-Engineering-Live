package com.telusko.service;

import com.telusko.model.Order;
import com.telusko.model.OrderItem;
import com.telusko.model.Product;
import com.telusko.model.dto.OrderItemRequest;
import com.telusko.model.dto.OrderItemResponse;
import com.telusko.model.dto.OrderRequest;
import com.telusko.model.dto.OrderResponse;
import com.telusko.repo.OrderRepo;
import com.telusko.repo.ProductRepo;
import jakarta.transaction.Transactional;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
public class OrderService {

    @Autowired
    private OrderRepo orderRepo;

    @Autowired
    private VectorStore vectorStore;

    @Autowired
    private ProductRepo productRepo;

    public OrderResponse placeOrder(OrderRequest request) {
        Order order = new Order();

        String uniqueOrderId = "ORD" + UUID.randomUUID().toString().replace("-", "").substring(0, 10).toUpperCase();
        order.setOrderId(uniqueOrderId);
        order.setCustomerName(request.customerName());
        order.setEmail(request.email());
        order.setOrderDate(LocalDate.now());
        order.setStatus("PLACED");

        List<OrderItem> orderItems = new ArrayList<>();

        for (OrderItemRequest itemReq : request.items()) {
            Product product = productRepo.findById(itemReq.productId())
                    .orElseThrow(() -> new RuntimeException("Product not found"));

            if (product.getStockQuantity() < itemReq.quantity()) {
                throw new RuntimeException("Insufficient stock for product: " + product.getName());
            }

            product.setStockQuantity(product.getStockQuantity() - itemReq.quantity());

            productRepo.save(product);

            String filter = String.format("productId == '%s'", String.valueOf(product.getId()));
            vectorStore.delete(filter);

            String updatedContent = String.format("""
                             Product Name: %s
                             Description: %s
                             Brand: %s
                             Category: %s
                             Price: %.2f
                             Release Date: %s
                             Available: %s
                             Stock: %d
                            """,
                    product.getName(),
                    product.getDescription(),
                    product.getBrand(),
                    product.getCategory(),
                    product.getPrice(),
                    product.getReleaseDate(),
                    product.isProductAvailable(),
                    product.getStockQuantity()
            );

            Document updatedDoc = new Document(
                    UUID.randomUUID().toString(),
                    updatedContent,
                    Map.of("productId", String.valueOf(product.getId()))
            );

            vectorStore.add(List.of(updatedDoc));


            OrderItem item = OrderItem.builder()
                    .product(product)
                    .quantity(itemReq.quantity())
                    .totalPrice(product.getPrice().multiply(BigDecimal.valueOf(itemReq.quantity())))
                    .order(order)
                    .build();

            orderItems.add(item);
        }

        order.setItems(orderItems);
        Order savedOrder = orderRepo.save(order);

        StringBuilder contentToEmbed = new StringBuilder();
        contentToEmbed.append("Order Summary:\n");
        contentToEmbed.append("Order ID: ").append(savedOrder.getOrderId()).append("\n");
        contentToEmbed.append("Customer: ").append(savedOrder.getCustomerName()).append("\n");
        contentToEmbed.append("Email: ").append(savedOrder.getEmail()).append("\n");
        contentToEmbed.append("Date: ").append(savedOrder.getOrderDate()).append("\n");
        contentToEmbed.append("Status: ").append(savedOrder.getStatus()).append("\n");
        contentToEmbed.append("Products:\n");

        for (OrderItem item : savedOrder.getItems()) {
            contentToEmbed.append("- ").append(item.getProduct().getName())
                    .append(" x ").append(item.getQuantity())
                    .append(" = ₹").append(item.getTotalPrice()).append("\n");
        }

        Document document = new Document(
                UUID.randomUUID().toString(),
                contentToEmbed.toString(),
                Map.of("orderId", savedOrder.getOrderId())
        );

        vectorStore.add(List.of(document));

        List<OrderItemResponse> itemResponses = savedOrder.getItems().stream()
                .map(i -> new OrderItemResponse(
                        i.getProduct().getName(),
                        i.getQuantity(),
                        i.getTotalPrice()))
                .collect(Collectors.toList());

        return new OrderResponse(
                savedOrder.getOrderId(),
                savedOrder.getCustomerName(),
                savedOrder.getEmail(),
                savedOrder.getStatus(),
                savedOrder.getOrderDate(),
                itemResponses
        );
    }


    @Transactional
    public List<OrderResponse> getAllOrderResponses() {
        List<OrderResponse> orders = new ArrayList<>();

        orderRepo.findAll().forEach(order -> {
            List<OrderItemResponse> itemResponses = order.getItems().stream()
                    .map(i -> new OrderItemResponse(
                            i.getProduct().getName(),
                            i.getQuantity(),
                            i.getTotalPrice()))
                    .toList();

            orders.add(new OrderResponse(
                    order.getOrderId(),
                    order.getCustomerName(),
                    order.getEmail(),
                    order.getStatus(),
                    order.getOrderDate(),
                    itemResponses));
        });

        return orders;
    }

}
