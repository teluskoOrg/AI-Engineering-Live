package com.telusko;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Ollama {
    public static void main(String[] args) throws IOException, InterruptedException {

        String uri = "http://localhost:11434/api/chat";

        String requestBody = """
        {
            "model": "mistral:latest",
            "messages": [
                {"role": "system", "content": "You are a movie review expert"},
                {"role": "user", "content": "name one movie for software engineers apart from social network, just the name"}
            ],
            "stream": false
        }
        """;

        HttpClient client = HttpClient.newHttpClient();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(uri))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());

    }
}