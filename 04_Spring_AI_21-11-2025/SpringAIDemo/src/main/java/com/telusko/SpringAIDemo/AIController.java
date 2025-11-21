package com.telusko.SpringAIDemo;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AIController {

//    private OpenAiChatModel chatModel;

//    public AIController(OpenAiChatModel chatModel) {
//        this.chatModel = chatModel;
//    }

    private ChatClient chatClient;

    public AIController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }


    @GetMapping("/api/greet/{message}")
    public String home(@PathVariable String message) {
        ChatResponse response = chatClient
                .prompt(message)
                .call()
                .chatResponse();
                //.content();

        String result = response.getResult().getOutput().getText();

        System.out.println(response.getMetadata());
        System.out.println(response.getMetadata().getUsage().getTotalTokens());

        return result;
    }
}
