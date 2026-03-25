<!-- Source: https://reference.langchain.com/python/langchain-classic/output_parsers/prompts/NAIVE_FIX -->

Attributev1.2.13 (latest)●Since v1.0

# NAIVE\_FIX


```
NAIVE_FIX = 'Instructions:\n--------------\n{instructions}\n--------------\nCompletion:\n--------------\n{completion}\n--------------\n\nAbove, the Completion did not satisfy the constraints given in the Instructions.\nError:\n--------------\n{error}\n--------------\n\nPlease try again. Please only respond with an answer that satisfies the constraints laid out in the Instructions:'
```


