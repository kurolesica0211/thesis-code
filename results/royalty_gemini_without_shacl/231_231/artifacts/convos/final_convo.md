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
Prince John of the United Kingdom (John Charles Francis; 12 July 1905 – 18 January 1919) was the fifth son and youngest of the six children of King George V and Queen Mary.
At the time of his birth, his father was heir apparent to John's grandfather Edward VII.
In 1910, John's father acceded to the throne upon Edward VII's death, and John became fifth in the line of succession to the British throne.
In 1909, it was discovered that John had epilepsy.
John's seclusion was subsequently brought forward as evidence of the royal family's inhumanity.
However, contrary to the belief that he was hidden from an early age, John was a fully-fledged member of the family for most of his life, appearing frequently in public until after his 11th birthday, when his condition became severe.
Birth

John was born at 3:05 am on 12 July 1905 at York Cottage on the Sandringham Estate, during the reign of his paternal grandfather, King Edward VII.
He was the youngest child and fifth son of George, Prince of Wales (later King George V), and Mary, Princess of Wales (later Queen Mary).
He was named John despite the name's traditionally unlucky associations within the royal family, and was informally known as Johnnie.
As a grandchild in the male line of the reigning British monarch, and a son of the Prince of Wales, he was formally styled His Royal Highness Prince John of Wales from birth until his father's accession to the throne in 1910.
John was christened on 3 August in the parish church of St Mary Magdalene at Sandringham, with the Reverend Canon John Neale Dalton officiating.
His godparents were King Carlos I of Portugal; his uncles Prince Carl of Denmark and Alexander Duff, 1st Duke of Fife; his great-granduncle Prince Johann of Schleswig-Holstein-Sonderburg-Glücksburg; and three of his first cousins once removed, the Duke and Duchess of Sparta, and Princess Alice, Countess of Athlone.
John's father stood proxy for King Carlos, Prince Carl, Prince Johann, and the Duke of Fife, while his aunt Princess Victoria stood proxy for the Duchess of Sparta and Princess Alice.
Childhood and illness

Much of John's early life was spent at Sandringham with his siblings – ​Prince Edward (known as David, later King Edward VIII), Prince Albert (known as Bertie, later King George VI), Princess Mary, Prince Henry, and Prince George – ​under the care of their nanny Charlotte "Lala" Bill.
In 1909, John's grandaunt, the Dowager Empress of Russia, wrote to her son Tsar Nicholas II that "George's children are very nice ...
The little ones, George and Johnny are both charming and very amusing".
John's aunt Princess Alice, Countess of Athlone described him as "very quaint and one evening when Uncle George returned from stalking he bent over Aunt May and kissed her, and they heard Johnny soliloquize, 'She kissed Papa, ugly old man!'"
George V once told U.S. President Theodore Roosevelt that "all  children  obedient, except John" – ​apparently because he alone, among the royal children, escaped punishment from their father.
Though a "large and handsome" baby, John had become "winsome" and "painfully slow" by his fourth birthday.
When his father became king, John did not attend his parents' coronation on 22 June 1911, as this was considered too risky for his health; cynics suggested that the family feared their reputation might be damaged by any incident involving him.
Although John was deemed not "presentable to the outside world," the king continued to show interest in him, offering him "kindness and affection".
During his years at Sandringham, John exhibited repetitive behaviours as well as regular misbehaviour and insubordination; as one account put it, "he simply didn't understand he needed to .
"


In 1912, Prince George, John's closest sibling, began St Peter's Court Preparatory School in Broadstairs.
The following summer, The Times reported that John would not attend Broadstairs the next term, and that the King and Queen had not yet decided whether to send him to school at all.
After the outbreak of World War I, John rarely saw his parents, who were often away on official duties, or his siblings, who were either at boarding school or serving in the military.
Wood Farm

In 1916, as his seizures became more frequent and severe, John was sent to live at Wood Farm, where Bill assumed responsibility for his care.
At Wood Farm, John became, in the words of one biographer, "a satellite with his own little household on an outlying farm on the Sandringham estate ...
"


After the summer of 1916, John was rarely seen outside the Sandringham estate and passed entirely into Bill's care.
When Queen Alexandra wrote that John "is very proud of his house but is longing for a companion", Queen Mary departed from usual royal practice by arranging for local children to be brought in as playmates.
One of these was Winifred Thomas, a young girl from Halifax who had been sent to live with her aunt and uncle, who managed the royal stables at Sandringham, in the hope that her asthma would improve.
John had known Winifred years earlier, before World War I.
John also played with his elder siblings during their visits; on one occasion, when his two eldest brothers came to see him, the Prince of Wales "took him for a run in a kind of a push-cart, and they both disappeared from view.
"


Death

John's seizures intensified, and Bill later wrote "we dared not let him be with his brothers and sister, because it upsets them so much, with the attacks getting so bad and coming so often."
Biographer Denis Judd writes that John's "seclusion and "abnormality" must have been disturbing to his brothers and sister", noting that he had been "a friendly, outgoing little boy, much loved by his brothers and sister, a sort of mascot for the family".
On 18 January 1919, after a severe seizure, John died in his sleep at Wood Farm at 5:30 pm, aged 13.
Queen Mary wrote in her diary that the news was:

a great shock, tho' for the poor little boy's restless soul, death came as a great relief.
broke the news to George and  motored down to Wood Farm.
Mary later wrote to Emily Alcock, an old friend, that:

for  it is a great relief, as his malady was becoming worse as he grew older, & he has thus been spared much suffering.
George described his son's death as "the greatest mercy possible".
On 20 January, the Daily Mirror reported that "when the Prince passed away his face bore an angelic smile"; the article also made the first public mention of John's epilepsy.
His funeral took place the next day at St Mary Magdalene parish church, with John Neale Dalton officiating.
Queen Mary wrote:

Canon Dalton & Dr Brownhill  conducted the service which was awfully sad and touching.
Queen Alexandra wrote to Queen Mary that "now  two darling Johnnies lie side by side".
Legacy


Edward, who was 11 years older than John and had hardly known him, regarded his brother's death as "little more than a regrettable nuisance."
He wrote an insensitive letter to Queen Mary, now lost, to which she did not reply.
In her final diary reference to John, Mary wrote simply: "miss the dear child very much indeed."
She gave Winifred Thomas several of John's books, inscribed "In memory of our dear little Prince."
Bill kept a portrait of John above her mantelpiece, together with a letter from him that read "nanny, I love you."
In the 21st century, John's seclusion has been cited as evidence of the Windsors' "heartlessness".
One author has written that the royal family believed such afflictions might pass through their blood, which was then still regarded as purer than that of a commoner, and therefore wished to conceal as much as possible about John's illness.
Others have suggested that John was sent to Wood Farm to provide him with the best environment available under the "austere" conditions of World War I.
Another author has stated that the family were "frightened and ashamed of John's illness", while yet another has noted that John's life is "usually portrayed either as tragedy or conspiracy".
At the time of Edward VIII's abdication, an attempt was made to discredit Albert, now George VI, by implying that he suffered from falling fits like John.
In 1998, the discovery of two volumes of family photographs briefly returned John to public attention.
The Lost Prince, a biographical drama about John's life written and directed by Stephen Poliakoff, was released in 2003.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (45a1b4c0-0ccb-4865-a212-32ff13f87d4b)
 Call ID: 45a1b4c0-0ccb-4865-a212-32ff13f87d4b
  Args:
    type: :Person
    source: Prince_John
  AssignClass (7a39678a-198b-4330-9496-56823f38c25b)
 Call ID: 7a39678a-198b-4330-9496-56823f38c25b
  Args:
    source: Prince_John
    type: :Man
  AddLiteral (fa170d7c-6b00-4682-92e2-99fefb7bdd11)
 Call ID: fa170d7c-6b00-4682-92e2-99fefb7bdd11
  Args:
    source: Prince_John
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1905
  AddLiteral (50c707a7-3f1c-479a-b632-6f01c3039fb5)
 Call ID: 50c707a7-3f1c-479a-b632-6f01c3039fb5
  Args:
    literal_value: 1919
    relation: :hasDeathYear
    source: Prince_John
    literal_type: xsd:integer
  AddLiteral (03f0860e-d96c-4751-8c58-58f044441c83)
 Call ID: 03f0860e-d96c-4751-8c58-58f044441c83
  Args:
    relation: :knownAs
    literal_value: Johnnie
    literal_type: xsd:string
    source: Prince_John
  AssignClass (391177e0-c17e-4211-b850-045ca295a2ec)
 Call ID: 391177e0-c17e-4211-b850-045ca295a2ec
  Args:
    source: King_George_V
    type: :Person
  AssignClass (3c8ecc44-0c97-4fe8-8dbd-8eb01ef21117)
 Call ID: 3c8ecc44-0c97-4fe8-8dbd-8eb01ef21117
  Args:
    type: :Man
    source: King_George_V
  AssignClass (67d890f1-2f6d-499f-8b67-023ed4310b8f)
 Call ID: 67d890f1-2f6d-499f-8b67-023ed4310b8f
  Args:
    type: :Person
    source: Queen_Mary
  AssignClass (1c098780-efe3-4c23-b4c1-af76ae3aaceb)
 Call ID: 1c098780-efe3-4c23-b4c1-af76ae3aaceb
  Args:
    source: Queen_Mary
    type: :Woman
  AddTriple (7456ec91-e01f-4b8b-bbb6-cd3fb260b19c)
 Call ID: 7456ec91-e01f-4b8b-bbb6-cd3fb260b19c
  Args:
    relation: :hasFather
    target: King_George_V
    source: Prince_John
  AddTriple (b595d046-c61a-494a-81b1-d8368759d7a0)
 Call ID: b595d046-c61a-494a-81b1-d8368759d7a0
  Args:
    relation: :hasMother
    source: Prince_John
    target: Queen_Mary
  AssignClass (30f74f20-56be-46c9-9a37-913869d50b62)
 Call ID: 30f74f20-56be-46c9-9a37-913869d50b62
  Args:
    type: :Person
    source: Edward_VII
  AssignClass (4617d712-a597-43cb-b066-300897530253)
 Call ID: 4617d712-a597-43cb-b066-300897530253
  Args:
    type: :Man
    source: Edward_VII
  AddTriple (3bcb39d0-62b7-46de-9c1f-a01b4deae91f)
 Call ID: 3bcb39d0-62b7-46de-9c1f-a01b4deae91f
  Args:
    relation: :isFatherOf
    source: Edward_VII
    target: King_George_V
  AssignClass (e1088379-479d-46b6-81bc-0a7946d7c795)
 Call ID: e1088379-479d-46b6-81bc-0a7946d7c795
  Args:
    source: Prince_Edward
    type: :Person
  AssignClass (3d0b3a2c-5be9-45ef-a2b1-c8934fa28d03)
 Call ID: 3d0b3a2c-5be9-45ef-a2b1-c8934fa28d03
  Args:
    type: :Man
    source: Prince_Edward
  AssignClass (f2fb4d9a-e686-4d88-9023-dd5b0f296278)
 Call ID: f2fb4d9a-e686-4d88-9023-dd5b0f296278
  Args:
    source: Prince_Albert
    type: :Person
  AssignClass (ccacd79c-c69e-4608-b4fa-37c5bb4d9c92)
 Call ID: ccacd79c-c69e-4608-b4fa-37c5bb4d9c92
  Args:
    type: :Man
    source: Prince_Albert
  AssignClass (14bc94ac-ee49-462f-8085-3b45937e0d05)
 Call ID: 14bc94ac-ee49-462f-8085-3b45937e0d05
  Args:
    source: Princess_Mary
    type: :Person
  AssignClass (42adaea4-f7b3-4c1e-a133-a1b7a730d6d9)
 Call ID: 42adaea4-f7b3-4c1e-a133-a1b7a730d6d9
  Args:
    type: :Woman
    source: Princess_Mary
  AssignClass (28b43024-a01f-4f6d-ae99-3b7541739115)
 Call ID: 28b43024-a01f-4f6d-ae99-3b7541739115
  Args:
    type: :Person
    source: Prince_Henry
  AssignClass (ae3ce661-d6ce-495d-afd3-9eaf8666d357)
 Call ID: ae3ce661-d6ce-495d-afd3-9eaf8666d357
  Args:
    type: :Man
    source: Prince_Henry
  AssignClass (25f3efa6-6b2e-4f7d-a2c4-777db511f160)
 Call ID: 25f3efa6-6b2e-4f7d-a2c4-777db511f160
  Args:
    source: Prince_George
    type: :Person
  AssignClass (9eac2449-41bd-4692-acef-a4fd99de7cac)
 Call ID: 9eac2449-41bd-4692-acef-a4fd99de7cac
  Args:
    type: :Man
    source: Prince_George
  AddTriple (b2738d3b-0676-422c-8986-348b2c7b2813)
 Call ID: b2738d3b-0676-422c-8986-348b2c7b2813
  Args:
    target: Prince_Edward
    source: Prince_John
    relation: :isSiblingOf
  AddTriple (73ad23e4-af20-4b21-bc9b-63f1444be724)
 Call ID: 73ad23e4-af20-4b21-bc9b-63f1444be724
  Args:
    source: Prince_John
    target: Prince_Albert
    relation: :isSiblingOf
  AddTriple (c61099ec-7a0f-4fa5-a748-a426db19094b)
 Call ID: c61099ec-7a0f-4fa5-a748-a426db19094b
  Args:
    target: Princess_Mary
    source: Prince_John
    relation: :isSiblingOf
  AddTriple (ecd4938c-9e7a-4cd8-bea9-df82ebd1d397)
 Call ID: ecd4938c-9e7a-4cd8-bea9-df82ebd1d397
  Args:
    relation: :isSiblingOf
    target: Prince_Henry
    source: Prince_John
  AddTriple (871400fb-bc96-4526-a551-e8813e5cbb4a)
 Call ID: 871400fb-bc96-4526-a551-e8813e5cbb4a
  Args:
    target: Prince_George
    source: Prince_John
    relation: :isSiblingOf
  Finish (d636feb1-8b89-4433-b38f-15bf301aa17d)
 Call ID: d636feb1-8b89-4433-b38f-15bf301aa17d
  Args: