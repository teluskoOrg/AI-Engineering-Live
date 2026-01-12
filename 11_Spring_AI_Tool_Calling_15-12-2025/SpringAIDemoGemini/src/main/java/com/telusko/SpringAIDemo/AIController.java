package com.telusko.SpringAIDemo;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.client.advisor.vectorstore.QuestionAnswerAdvisor;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.ai.chat.memory.MessageWindowChatMemory;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.chat.prompt.PromptTemplate;
import org.springframework.ai.document.Document;
import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
public class AIController {

    private ChatClient chatClient;
    private ChatMemory  memory = MessageWindowChatMemory.builder().build();

    @Autowired
    @Qualifier("googleGenAiTextEmbedding")
    private EmbeddingModel embeddingModel;

    @Autowired
    private VectorStore vectorStore;

    @Autowired
    private DateTimeTool dateTimeTool;

    public AIController(ChatClient.Builder builder) {
        this.chatClient = builder
                .defaultAdvisors(MessageChatMemoryAdvisor.builder(memory).build())
                .build();
    }


    @GetMapping("/api/{message}")
    public String home(@PathVariable String message) {
        ChatResponse response = chatClient
                .prompt(message)
                .tools(dateTimeTool,new NewsTool())
                .call()
                .chatResponse();  //.content();

        String result = response.getResult().getOutput().getText();

//        System.out.println(response.getMetadata());
//        System.out.println(response.getMetadata().getUsage().getTotalTokens());

        System.out.println(response);

        return result;
    }


    @GetMapping("/api/movie")
    public String getMovie(@RequestParam String type, @RequestParam String year, @RequestParam String lang){

        String tempt = """
                I want to watch a {type} movie with a good rating,
                  released around {year} in {lang} language,
                  suggest one specific movie and tell me the cast and length of the movie.
                
                response format should be:
                Movie name: <name>
                Cast: <cast>
                Length: <length>
                IMDB rating: <rating>
                Basic Plot: <plot>
                """;

        PromptTemplate template = PromptTemplate.builder()
                .template(tempt)
                .build();

        Prompt prompt = template.create(Map.of("type", type, "year", year, "lang", lang));

        String result = chatClient
                .prompt(prompt)
                .call()
                .content();

        return result;
    }

    @GetMapping("/api/embedding")
    public float[] getVector(@RequestParam String text){

       return embeddingModel.embed(text);
    }

    @GetMapping("/api/similarity")
    public double cosineSimilarity(@RequestParam String text1, @RequestParam String text2){

        float[] embed1 = embeddingModel.embed(text1);
        float[] embed2 = embeddingModel.embed(text2);

        double dotProduct = 0.0;
        double normA = 0.0;
        double normB = 0.0;
        for (int i = 0; i < embed1.length; i++) {
            dotProduct += embed1[i] * embed2[i];
            normA += Math.pow(embed1[i], 2);
            normB += Math.pow(embed2[i], 2);
        }
        return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB)) * 100;
    }

    @GetMapping("/api/products")
    public List<Document> getProducts(@RequestParam String text){

//        return vectorStore.similaritySearch(text);

        return vectorStore.similaritySearch(SearchRequest.builder()
                        .query(text)
                        .topK(2)
                        .build());
    }

    @GetMapping("/api/ask/{query}")
    public String productInfo(@PathVariable String query) {

        // Retrieval
        List<Document> docs = vectorStore.similaritySearch(query);

        // Augmentation
        StringBuilder context = new StringBuilder();
        for (Document doc : docs) {
            context.append(doc.getFormattedContent()).append("\n");
        }

        // Generation
        String prompt = """
                         You are a helpful product suggestion assistant.
                Use only the information in the product details below to answer the user.
                If the information is not available there, say you don't know.
                Product details:
                %s
                User question: %s
                Answer in a short, clear way with price and other relevant details:
                """.formatted(context, query);

        return chatClient.prompt(prompt).call().content();


        // Automatic RAG
       /* String template = """
                 {query}
                 Context information is below.
                -------------------------------
                {question_answer_context}
                -------------------------------
                Given the context information and no prior knowledge, answer the query with name and price
                , category and description.
                
                Follow these rules:
                1. If the answer is not in the context, just say that you don't know.
                2. Avoid statements like "Based on the context..." or "The provided information....".
                """;

        PromptTemplate promptTemplate = PromptTemplate.builder()
                .template(template)
                .build();


        return chatClient
                .prompt(query)
                .advisors(QuestionAnswerAdvisor
                        .builder(vectorStore)
                        .promptTemplate(promptTemplate)
                        .build())
                .call()
                .content();*/
    }
}
