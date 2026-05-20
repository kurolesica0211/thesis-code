================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Margaret of Prussia (German: Margarethe Beatrice Feodora; 22 April 1872 – 22 January 1954) was the youngest child of Frederick III, German Emperor, and Victoria, Princess Royal.
She was also the younger sister of Emperor Wilhelm II and the granddaughter of Queen Victoria.
She married Prince Frederick Charles of Hesse, the elected King of Finland, making her the would-be Queen of Finland had he not decided to renounce the throne on 14 December 1918.
In 1926, they assumed the titles of Landgrave and Landgravine of Hesse.
Early life

Princess Margaret of Prussia was the youngest of eight children born to Frederick III, then Crown Prince of the German Empire, and Victoria, Princess Royal, Britain's Queen Victoria's eldest daughter.
Born on 22 April 1872 in the Hohenzollerns' New Palace in Potsdam, by the time the infant was christened, her head was covered with short hair like moss, from which she acquired her nickname "Mossy".
Crown Princess Margherita of Italy was her godmother and Emperor Pedro II of Brazil was her godfather.
Princess Margaret grew up amid great privilege and formality.
Together with her sisters, Princess Viktoria and Princess Sophie, Margaret was deeply attached to her parents, forming an antagonist group to that of her eldest siblings, William II, Princess Charlotte and Prince Henry.
Margaret was widely regarded as the most popular of Kaiser Wilhelm II's sisters, and she maintained good relations with a wide array of family members.
She was the first cousin of both King George V of the United Kingdom and Empress Alexandra of Russia, all three being grandchildren of Victoria.
As an adult, she was said to resemble her aunt, Princess Alice.
Marriage

Princess Margaret was first attracted to Prince Maximilian of Baden.
When he did not reciprocate her affection, she moved on to her second choice, Max's close friend, Prince Frederick Charles of Hesse, future head of the Hesse-Kassel dynasty and future elected King of Finland.
At the time of the wedding, Prince Frederick Charles was not the Head of the House of Hesse-Kassel.
Prince Frederick Charles, as was his title when he married, was addressed as His Highness, while Princess Margaret warranted Royal Highness.
This disparity came to an end in 1925 when Frederick Charles became Landgrave of Hesse and Head of the house of Hesse-Kassel.
They were second cousins, both great-grandchildren of King Friedrich Wilhelm III of Prussia, he through his mother Anna, she through her father Friedrich.
Initially, her brother Wilhelm opposed the match as he felt that Frederick Charles's position was too "minor" for the Kaiser's sister.
Later, however, he gave his blessing, since Margaret herself "was so unimportant".
Princess Margaret had a strong personality; she always seemed more secure and grounded than her husband.
Margaret's husband was her mother's favorite son-in-law.
In 1901, Princess Margaret inherited Schloss Friedrichshof at the death of her mother.
However, Margaret was committed to maintain the house of her mother which entailed a great expense and the family moved to Friedrichshof.
In 1918, Margaret's husband accepted the offer of the throne of newly independent Finland, but due to German misfortunes in World War I, soon renounced it.
Family tragedies

Margaret's elder sons, Friedrich Wilhelm and Maximilian, were killed in action during World War I. Prince Maximilian, Princess Margaret's second and favorite son, was serving near Aisne when he was seriously wounded by machine gun fire in October 1914.
Princess Margaret's oldest son, Friedrich Wilhelm, died on 12 September 1916 at Kara Orman in Romania.
Her two other sons, Philipp and Christoph, embraced Nazism, and Margaret, who was the sister of the last Kaiser Wilhelm II, invited Adolf Hitler to tea and flew the swastika from her home at Schloss Kronberg.
Philipp married Princess Mafalda, daughter of King Victor Emmanuel III of Italy.
Margaret's fifth son, Christoph, was a staunch supporter of the German war effort, but after the Battle of Stalingrad, he became frustrated by the limitations placed on his own role in the conflict, and increasingly critical of the German leadership.
Christoph's reaction to the assassination of Heydrich, whom he called a "dangerous and cruel man", in 1942 was that it was "the best news I had in a long time".
He was married to Princess Sophie of Greece, sister of Philip, Prince of Greece and Denmark who, in 1947, married the heir to the throne of the United Kingdom and, in 1952, became Prince Philip, Duke of Edinburgh, consort of Queen Elizabeth II.
Margaret also lost another one of her daughters-in-law during the war.
Wolfgang's wife, Princess Marie Alexandra, when she and seven other women war aid workers, were killed in a bomb attack on Frankfurt on 29–30 January 1944.
Margaret, very much the matriarch, was at the centre of her large and dynamic family.
Last years

Landgravine Margaret had difficult years after 1945; they were compounded by the theft from Schloss Friedrichshof in November 1945 of the family jewellery, valued at over £2,000,000.
Princess Margaret's son Wolfgang, fearing for the jewels, had buried them in a sub-cellar of the castle.
In early 1946, Princess Margaret discovered the theft when the family wanted to use the jewels for the wedding of Princess Sophia who was preparing to remarry.
Princess Sophia and Landgravine Margaret reported it to the Frankfurt authorities, and the culprits were imprisoned in August 1951.
The Hesse family received what had been recovered: only 10 percent of what had been stolen.
Landgravine Margaret, the last surviving child of Emperor Frederick III and last grandchild of emperor Emperor Wilhelm I, died in Kronberg on 22 January 1954, 14 years after her husband and exactly 53 years to the day after her British grandmother Queen Victoria.
Children

Landgravine Margaret and her husband Frederick Charles of Hesse had six sons, including two sets of twins:


Archives

Margaret's personal papers (including family correspondence) are preserved in the Archive of the House of Hesse, which is kept in Fasanerie Palace in Eichenzell, Germany.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (b954f9c9-c413-457a-b19a-33c7d12d5bc0)
 Call ID: b954f9c9-c413-457a-b19a-33c7d12d5bc0
  Args:
    type: :Woman
    source: Margaret_of_Prussia
  AssignClass (6b7367c8-4415-489d-b780-6295c3ad56c0)
 Call ID: 6b7367c8-4415-489d-b780-6295c3ad56c0
  Args:
    type: :Man
    source: Frederick_III
  AssignClass (395fb25c-cf43-4701-aa76-67c2ba533a2d)
 Call ID: 395fb25c-cf43-4701-aa76-67c2ba533a2d
  Args:
    type: :Woman
    source: Victoria_Princess_Royal
  AssignClass (82d9e48c-50c7-4001-8f6a-c487bd0fa9e9)
 Call ID: 82d9e48c-50c7-4001-8f6a-c487bd0fa9e9
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (8ba4fbb0-c9e2-4ee4-8de0-4c7ad6b91506)
 Call ID: 8ba4fbb0-c9e2-4ee4-8de0-4c7ad6b91506
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (900135f5-ffa2-416d-862a-0d9035c4b0ba)
 Call ID: 900135f5-ffa2-416d-862a-0d9035c4b0ba
  Args:
    type: :Man
    source: Frederick_Charles_of_Hesse
  AddLiteral (a7838c64-6b9b-4980-bc89-6f27791574bf)
 Call ID: a7838c64-6b9b-4980-bc89-6f27791574bf
  Args:
    relation: :alsoKnownAs
    literal_value: Margarethe Beatrice Feodora
    source: Margaret_of_Prussia
    literal_type: xsd:string
  AddLiteral (ea843f4b-5f08-4923-91ca-2845d45dd327)
 Call ID: ea843f4b-5f08-4923-91ca-2845d45dd327
  Args:
    literal_type: xsd:integer
    source: Margaret_of_Prussia
    literal_value: 1872
    relation: :hasBirthYear
  AddLiteral (c53880a9-eed4-4c69-8956-4798c9d425ea)
 Call ID: c53880a9-eed4-4c69-8956-4798c9d425ea
  Args:
    relation: :hasDeathYear
    source: Margaret_of_Prussia
    literal_value: 1954
    literal_type: xsd:integer
  AddTriple (50d5fe76-eeae-4ea3-a076-2486dfb1493a)
 Call ID: 50d5fe76-eeae-4ea3-a076-2486dfb1493a
  Args:
    target: Frederick_III
    source: Margaret_of_Prussia
    relation: :hasFather
  AddTriple (721281d5-75a5-4ed7-b274-0492ab4905c9)
 Call ID: 721281d5-75a5-4ed7-b274-0492ab4905c9
  Args:
    source: Margaret_of_Prussia
    target: Victoria_Princess_Royal
    relation: :hasMother
  AddTriple (58b4a7b7-ba36-4734-ac8a-e2127cb2c79a)
 Call ID: 58b4a7b7-ba36-4734-ac8a-e2127cb2c79a
  Args:
    relation: :isSisterOf
    source: Margaret_of_Prussia
    target: Wilhelm_II
  AddTriple (f2cbf908-97d9-4ca6-a70f-dba121eb2317)
 Call ID: f2cbf908-97d9-4ca6-a70f-dba121eb2317
  Args:
    relation: :hasParent
    target: Queen_Victoria
    source: Victoria_Princess_Royal
  AddTriple (a87be01e-fa85-4b24-a1bd-9ce2ada52b0f)
 Call ID: a87be01e-fa85-4b24-a1bd-9ce2ada52b0f
  Args:
    source: Margaret_of_Prussia
    target: Queen_Victoria
    relation: :hasParent
  AddTriple (5f07eb62-9960-4dbd-9a6a-8da84103a218)
 Call ID: 5f07eb62-9960-4dbd-9a6a-8da84103a218
  Args:
    relation: :hasRelation
    source: Margaret_of_Prussia
    target: Frederick_Charles_of_Hesse
  AddLiteral (a247adf4-d6fd-48f0-adcc-a58ca0f4a36b)
 Call ID: a247adf4-d6fd-48f0-adcc-a58ca0f4a36b
  Args:
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Mossy
    source: Margaret_of_Prussia
  Finish (c2775b0f-df24-4b20-b676-c288a64d2e2c)
 Call ID: c2775b0f-df24-4b20-b676-c288a64d2e2c
  Args: