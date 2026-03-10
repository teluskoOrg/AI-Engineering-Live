package com.telusko.config;

import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.ai.vectorstore.mariadb.MariaDBVectorStore;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;

@Configuration
public class VectorStoreConfig {

    @Bean
    public VectorStore vectorStore(JdbcTemplate jdbcTemplate, EmbeddingModel embeddingModel) {
        return MariaDBVectorStore.builder(jdbcTemplate, embeddingModel)
                .dimensions(1536)
                .distanceType(MariaDBVectorStore.MariaDBDistanceType.COSINE)
                .initializeSchema(true)
                .vectorTableName("vector_store")
                .build();
    }
}
