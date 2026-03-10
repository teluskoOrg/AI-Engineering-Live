package com.telusko.service;

import org.springframework.ai.image.ImageModel;
import org.springframework.ai.image.ImagePrompt;
import org.springframework.ai.image.ImageResponse;
import org.springframework.ai.openai.OpenAiImageOptions;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.InputStream;
import java.net.URL;

@Service
public class AIImageGeneratorService {

    @Autowired
    private ImageModel imageModel;

    public byte[] generateImage(String prompt) {
        try {
            OpenAiImageOptions options = OpenAiImageOptions.builder()
                    .N(1)
                    .width(1024)
                    .height(1024)
                    .quality("standard")
                    .responseFormat("url")
                    .model("dall-e-3")
                    .build();

            ImageResponse response = imageModel.call(new ImagePrompt(prompt, options));

            String imageUrl = response.getResult().getOutput().getUrl();

            try (InputStream in = new URL(imageUrl).openStream()) {
                return in.readAllBytes();
            }

        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
