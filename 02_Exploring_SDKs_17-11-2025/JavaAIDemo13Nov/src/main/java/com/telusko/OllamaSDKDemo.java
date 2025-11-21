package com.telusko;

import io.github.ollama4j.OllamaAPI;
import io.github.ollama4j.exceptions.OllamaBaseException;
import io.github.ollama4j.models.response.OllamaResult;
import io.github.ollama4j.utils.Options;
import io.github.ollama4j.utils.OptionsBuilder;

import java.io.IOException;

public class OllamaSDKDemo {
    public static void main(String[] args) {

        String host = "http://localhost:11434/";

        OllamaAPI client = new OllamaAPI(host);

        String prompt = "name one comedy movie with Shah Rukh Khan, just the name";

        Options options = new OptionsBuilder().build();

        try {
            OllamaResult result = client.generate(
                    "mistral",
                    prompt,
                    false,
                    false,
                    options
            );

            System.out.println(result.getResponse());
        } catch (OllamaBaseException | IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
