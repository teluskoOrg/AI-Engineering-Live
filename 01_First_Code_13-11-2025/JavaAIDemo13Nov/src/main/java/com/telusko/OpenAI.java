package com.telusko;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class OpenAI {
    public static void main(String[] args) throws IOException, InterruptedException {

        String apiKey = System.getenv("OPENAI_API_KEY");
        String uri = "https://api.openai.com/v1/chat/completions";

        String requestBody = """
        {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": "You are a movie review expert"},
                {"role": "user", "content": "name one movie for software engineers apart from social network, just the name"}
            ]
        }
        """;

        HttpClient client = HttpClient.newHttpClient();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(uri))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + apiKey)
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());

    }
}