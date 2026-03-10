package com.telusko.service;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.prompt.PromptTemplate;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class ChatBotService {

    @Autowired
    private ChatClient chatClient;

    @Autowired
    private VectorStore vectorStore;

    @Autowired
    private ResourceLoader resourceLoader;

    public String getBotResponse(String userQuery) {
        try {
            String promptTemplate = Files.readString(
                    resourceLoader.getResource("classpath:prompts/chatbot-rag-prompt.st")
                            .getFile()
                            .toPath()
            );

            String context = fetchSemanticContext(userQuery);

            Map<String, Object> variables = new HashMap<>();
            variables.put("userQuery", userQuery);
            variables.put("context", context);

            PromptTemplate prompt = PromptTemplate.builder()
                    .template(promptTemplate)
                    .variables(variables)
                    .build();

            return chatClient.prompt(prompt.create()).call().content();

        } catch (IOException e) {
            return "Error: " + e.getMessage();
        }
    }

    private String fetchSemanticContext(String query) {
        List<Document> documents = vectorStore.similaritySearch(
                SearchRequest.builder()
                        .query(query)
                        .topK(5)
                        .build()
        );

        StringBuilder contextBuilder = new StringBuilder();
        for (Document doc : documents) {
            contextBuilder.append(doc.getFormattedContent()).append("\n");
        }

        return contextBuilder.toString();
    }
}
