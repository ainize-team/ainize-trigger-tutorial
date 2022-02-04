# Ainize Trigger Tutorial
This project shows the process of calling the API of a project deployed in Ainize using AI Network Blockchain. Here, we will intro the process of writing down the results from the model after setting the Trigger Function on Blockchain using the API of the model that was fine-tuned (GPT-2) with the novel Pride and Prejudice.

![](https://i.imgur.com/8VxLe38.png)

AI Network Blockchain, which can handle large-scale transactions, has been designed to securely record communications between clients as well as sending requests and nodes processing tasks. A more detailed description of AI Network Blockchain can be found [here](https://docs.ainetwork.ai/).

### How to use?
Check out [Ainize Trigger Tutorial](https://ai-network.gitbook.io/ainize-tutorials/tutorials-1/tutorial-for-ainize-trigger). In this tutorial, you will learn to:
1. Create an App on the AI Network Blockchain and register a Trigger Function through Ainize
2. Use the Trigger Function
3. Write Values on AI Network Blockchain

![](https://i.imgur.com/0zzaCwu.png)

If you want to use the **Trigger** of this project, please check the [link](https://ainize.ai/ainize-team/ainize-trigger-tutorial).

### How to set Database path?
In this project, the database path for triggers goes one step further into the depth of appName. For example, it should be something like `/apps/appName/input` , but I recommend the format `/apps/appName/$timestamp/input` for readability.  
![](https://i.imgur.com/ZI9Dga6.png)
Then, the value will be written to the path of `/apps/appName/$timestamp/result`
![](https://i.imgur.com/3JNzH8l.png)
