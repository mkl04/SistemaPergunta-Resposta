# [Sistema Pergunta-Resposta sobre a situação atual no Peru em textos de revistas usando redes Transformers](https://github.com/mkl04/SistemaPergunta-Resposta)


#### Aluno: [Maykol Jiampiers Campos Trinidad](https://github.com/mkl04)
#### Orientador: [Cristian Muñoz](https://github.com/crismunoz)

---

Trabalho apresentado ao curso BI MASTER como pré-requisito para conclusão de curso e obtenção de crédito na disciplina [Projetos de Sistemas Inteligentes de
Apoio à Decisão](https://ica.puc-rio.ai/es/bi-master-es/).

---

### Resumo

Dada a enorme quantidade de informações que são compartilhadas nas notícias, decidiu-se implementar um sistema de perguntas-respostas que permite responder a perguntas específicas sobre as notícias peruanas.

### 1. Introdução

Há muitos anos, os pesquisadores buscam criar um assistente virtual que possa entender a linguagem natural para automatizar tarefas como suporte a perguntas sobre temas específicos (closed-domain), ou até mesmo manter uma conversa quase humana. Esse processo de compreensão é conhecido como Natural Language Processing (NLP), que nos últimos anos, graças às redes neurais conhecidas como [Transformers](https://arxiv.org/abs/1706.03762), conseguiram grandes feitos. O último avanço que chamou a atenção foi o [GPT-3](https://arxiv.org/abs/2005.14165), um modelo que resolve diferentes tarefas de NLP para as quais não foi especificamente treinado.

Dado que a informação nos meios de comunicação aumenta a cada dia, decidiu-se implementar um sistema de perguntas e respostas que nos permita obter respostas sobre as notícias nacionais. Para isso, contamos com um modelo de deep learning baseado nas já mencionadas redes Transformers, e notícias peruanas extraídas com webscrapping. Parte da contribuição deste projeto foi demonstrar uma aplicação de deep learning interessante para a área de NLP, que pode ser replicada em qualquer computador, pois não requer GPUs.

### 2. Modelagem

A modelagem deste projeto está organizada em uma metodologia de trabalho composta por quatro etapas: i) Extração e pré-processamento de dados; ii) Information Retrieval; iii) Modelagem e inferência; e iv) Interface.

**i) Extração e pré-processamento de dados**

Para esta etapa, foi realizado o webscrapping da página de um respeitado jornal do Peru chamado [Gestión](https://gestion.pe/). As bibliotecas utilizadas foram BeautifulSoup (para gerenciamento de tags) e Selenium (para navegação de página, pois é dinâmica). Com o script `webscrapping.py` essa extração é feita, onde você pode definir a quantidade dos últimos dias dos quais essas notícias serão extraídas e salvas em um arquivo CSV. Este CSV salva o título da notícia, sua data, o texto total e a url. Para o processo de limpeza dos textos, foram eliminados apenas os caracteres especiais de pontuação, assim como as stopwords.

**ii) Information Retrieval**

É assim que se conhece o processo de seleção dos textos mais próximos da pergunta feita (consulta). Para esta etapa, foi utilizado o algoritmo mais conhecido: [BM25](https://en.wikipedia.org/wiki/Okapi_BM25) (best matching), que é uma função de recuperação de bag-of-words que classifica um conjunto de documentos com base nos termos de consulta que aparecem em cada documento, independentemente de sua proximidade dentro o documento. 

**iii) Modelagem e inferência**

O modelo usado é uma versão destilada do BETO (versão espanhol do BERT) com ajuste fino no conjunto de dados [SQuAD v2.0](https://rajpurkar.github.io/SQuAD-explorer/) traduzido para o espanhol que foi treinado para Q&A. O modelo está disponível na página do [Hugging Face](https://huggingface.co/), e tem como entradas tanto o contexto (notícia) quanto a pergunta.

Para a escolha da resposta, primeiro são escolhidas as 5 notícias mais relacionadas à pergunta inserida (query) que foram obtidos do BM25. Como o modelo dá uma pontuação de quão certo está de sua resposta, a resposta que deu a melhor pontuação é escolhida. Para reduzir o tempo de inferência, foi estabelecido um threshold de forma que, caso o escore de uma resposta ultrapasse esse valor, essa resposta seja escolhida.


**iv) Interface**

O template foi obtido do [Web App da IBM](https://github.com/IBM/MAX-Question-Answering-Web-App). Isso permite uma comunicação mais dinâmica com os usuários. O usuário pode inserir quantas perguntas quiser. O sistema foi atualizado e agora pode fazer as inferências usando CPU ou GPU. No caso de usar CPU, a inferência pode demorar um pouco.
Para inicializar o sistema, só precisa rodar o comando do seguinte jeito:
```
python app.py
```
Depois disso, deve acessar a url `http://localhost:8070/` no seu navegador onde podera visualizar o chatbot.

### 3. Resultados

Como pode ser visto na imagem, o chatbot consegue responder corretamente para as perguntas de exemplo. Além disso, mostra um percentual de precisão de inferência para saber o quão confiável foi essa resposta. Obviamente, este aplicativo nem sempre mostra a resposta certa, mas talvez com um ajuste fino, podeeria conseguir melhorar a certeza.

![Algumas perguntas feitas](imgs/results.PNG?raw=true "Demo")

### 4. Conclusões

Podemos concluir que o aplicativo consegue responder corretamente algumas questões específicas do panorama atual do Peru, mas que precisa de um ajuste fino para melhorar esse desempenho. Por outro lado, como passo futuro, um algoritmo mais robusto poderia ser buscado para a tarefa de Information Retrieval.

---

Matrícula: 201.190.254

Pontifícia Universidade Católica do Rio de Janeiro

Curso de Pós Graduação Business Intelligence Master