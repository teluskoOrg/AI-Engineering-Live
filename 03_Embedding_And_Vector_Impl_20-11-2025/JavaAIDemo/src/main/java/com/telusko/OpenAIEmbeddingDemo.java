package com.telusko;

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.embeddings.CreateEmbeddingResponse;
import com.openai.models.embeddings.Embedding;
import com.openai.models.embeddings.EmbeddingCreateParams;

import java.util.List;

public class OpenAIEmbeddingDemo {
    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.fromEnv();

        List<String> words = List.of(
                "cat", "Dog", "Fish", "laptop", "Java", "Python",
                "King", "Queen", "Apple", "Banana", "Mars", "Kitty"
        );

        for (String word : words) {
            EmbeddingCreateParams params = new EmbeddingCreateParams.Builder()
                    .model("text-embedding-3-large")
                    .input(word)
                    .dimensions(2)
                    .build();

            CreateEmbeddingResponse response = client.embeddings().create(params);
            Embedding embedding = response.data().get(0);

            System.out.printf("%s = (%.6f, %.6f)%n",
                    word,
                    embedding.embedding().get(0),
                    embedding.embedding().get(1));
        }

    }
}