package com.telusko;

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

public class OpenAISDKDemo {
    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.fromEnv();

        ResponseCreateParams params = ResponseCreateParams.builder()
                .input("name one movie comedy movie with Srk, just the name")
                .model("gpt-5")
                .build();

        Response response = client.responses().create(params);
        System.out.println(response);
    }
}
