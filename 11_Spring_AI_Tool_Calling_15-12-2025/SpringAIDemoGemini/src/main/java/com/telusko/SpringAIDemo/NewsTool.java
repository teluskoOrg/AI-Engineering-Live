package com.telusko.SpringAIDemo;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class NewsTool {

    private RestTemplate restTemplate = new RestTemplate();

    @Tool(description = "Get current news haedlines for specific topic")
    public String getNewsHeadlines(String topic){

        String apiKey = "<YOUR API KEY>";
        String url = "https://newsapi.org/v2/everything?q=" + topic + "&apiKey=" + apiKey;

        String result = restTemplate.getForObject(url, String.class);
        System.out.println(result);


        return result;
//        return "News Headlines for topic " + topic;

    }
}
