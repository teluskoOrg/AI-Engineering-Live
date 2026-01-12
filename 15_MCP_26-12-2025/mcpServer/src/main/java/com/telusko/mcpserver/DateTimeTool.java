package com.telusko.mcpserver;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;

@Component
public class DateTimeTool {

    @Tool(description = "Get Current date and time for user's timezone")
    public String getCurrentDateAndTime(){
        System.out.println("in local timezone");
        return ZonedDateTime.now().toString();
    }

    @Tool(description = "Get Current date and time for user's timezone")
    public String getCurrentDateAndTimeTimeZoned(String timezone){
        System.out.println("in specified timezone");
        return ZonedDateTime.now(ZoneId.of(timezone)).toString();
    }
}