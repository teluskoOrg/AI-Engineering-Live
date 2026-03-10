package com.telusko.model.dto;

public record OrderItemRequest(
        int productId,
        int quantity
) {}
