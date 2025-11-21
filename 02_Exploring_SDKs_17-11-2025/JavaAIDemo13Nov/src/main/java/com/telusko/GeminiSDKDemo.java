package com.telusko;

import com.google.genai.Client;
import com.google.genai.types.GenerateContentResponse;

public class GeminiSDKDemo {
    public static void main(String[] args) {
        Client client = new Client();

        GenerateContentResponse response =
                client.models.generateContent(
                        "gemini-2.5-flash",
                        "name one movie comedy movie with Srk, just the name",
                        null);

        System.out.println(response.text());
    }
}

// Set ENV:
//GOOGLE_API_KEY = <GEMINI-API-KEY>