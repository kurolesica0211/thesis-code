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
  AssignClass (5d216b21-82c2-4c5a-b737-dad11bbe4d77)
 Call ID: 5d216b21-82c2-4c5a-b737-dad11bbe4d77
  Args:
    source: Prince_John
    type: :Man
  AssignClass (33602f51-5485-4a31-be1e-1348ef8fb14a)
 Call ID: 33602f51-5485-4a31-be1e-1348ef8fb14a
  Args:
    type: :Person
    source: Prince_John
  AddLiteral (5b608a3b-c384-4bf3-955d-7f70031765b1)
 Call ID: 5b608a3b-c384-4bf3-955d-7f70031765b1
  Args:
    relation: :hasBirthYear
    source: Prince_John
    literal_type: xsd:integer
    literal_value: 1905
  AddLiteral (d977dc25-3a53-4b73-8762-c064a2e89952)
 Call ID: d977dc25-3a53-4b73-8762-c064a2e89952
  Args:
    literal_value: 1919
    literal_type: xsd:integer
    source: Prince_John
    relation: :hasDeathYear
  AddLiteral (0791b5c9-f1b6-4d3c-a4d2-ac618160880e)
 Call ID: 0791b5c9-f1b6-4d3c-a4d2-ac618160880e
  Args:
    relation: :alsoKnownAs
    source: Prince_John
    literal_type: xsd:string
    literal_value: Johnnie
  AssignClass (e078670e-1505-4da0-8c91-7b9ffea5f511)
 Call ID: e078670e-1505-4da0-8c91-7b9ffea5f511
  Args:
    type: :Man
    source: King_George_V
  AssignClass (f1edda14-fd0f-49c2-a772-1323303a0b99)
 Call ID: f1edda14-fd0f-49c2-a772-1323303a0b99
  Args:
    type: :Person
    source: King_George_V
  AssignClass (6863f6a2-222e-48d0-a31c-3d2c6a0e6275)
 Call ID: 6863f6a2-222e-48d0-a31c-3d2c6a0e6275
  Args:
    type: :Woman
    source: Queen_Mary
  AssignClass (e826e502-b872-401b-a548-0d5fa5908354)
 Call ID: e826e502-b872-401b-a548-0d5fa5908354
  Args:
    type: :Person
    source: Queen_Mary
  AddTriple (7e99324a-a507-44f1-9e50-94e065190eea)
 Call ID: 7e99324a-a507-44f1-9e50-94e065190eea
  Args:
    source: Prince_John
    relation: :hasFather
    target: King_George_V
  AddTriple (bf9c3806-b55c-4232-87a4-d00ee61cb28b)
 Call ID: bf9c3806-b55c-4232-87a4-d00ee61cb28b
  Args:
    target: Queen_Mary
    relation: :hasMother
    source: Prince_John
  AssignClass (e50dd33f-093f-47dc-80ab-66953b9e6c47)
 Call ID: e50dd33f-093f-47dc-80ab-66953b9e6c47
  Args:
    type: :Man
    source: Edward_VII
  AssignClass (49a79db4-8493-44f8-bd9d-82d4842507d2)
 Call ID: 49a79db4-8493-44f8-bd9d-82d4842507d2
  Args:
    source: Edward_VII
    type: :Person
  AddTriple (30172998-6481-4a83-9559-e8ded4f3f0c3)
 Call ID: 30172998-6481-4a83-9559-e8ded4f3f0c3
  Args:
    relation: :hasFather
    target: Edward_VII
    source: King_George_V
  AssignClass (e4d5c5a8-0037-450d-a7d8-44de205948f9)
 Call ID: e4d5c5a8-0037-450d-a7d8-44de205948f9
  Args:
    type: :Man
    source: Prince_Edward
  AssignClass (c547fd43-582d-479f-a786-e1ac386a952b)
 Call ID: c547fd43-582d-479f-a786-e1ac386a952b
  Args:
    source: Prince_Edward
    type: :Person
  AssignClass (2b700ba6-2f06-4e40-b0d4-c13951d8e38e)
 Call ID: 2b700ba6-2f06-4e40-b0d4-c13951d8e38e
  Args:
    source: Prince_Albert
    type: :Man
  AssignClass (0c2d374a-2106-4ab2-8473-6bc534a2f565)
 Call ID: 0c2d374a-2106-4ab2-8473-6bc534a2f565
  Args:
    source: Prince_Albert
    type: :Person
  AssignClass (58135fa4-6a46-47b1-9f72-b796651a4b34)
 Call ID: 58135fa4-6a46-47b1-9f72-b796651a4b34
  Args:
    type: :Woman
    source: Princess_Mary
  AssignClass (79d3ca67-e1e0-4b7f-9be8-63a44b218eeb)
 Call ID: 79d3ca67-e1e0-4b7f-9be8-63a44b218eeb
  Args:
    type: :Person
    source: Princess_Mary
  AssignClass (8dbaee59-96f7-4ea9-8256-717b881d9073)
 Call ID: 8dbaee59-96f7-4ea9-8256-717b881d9073
  Args:
    type: :Man
    source: Prince_Henry
  AssignClass (95e194f8-ac6c-47cf-baca-85bfb81f80e4)
 Call ID: 95e194f8-ac6c-47cf-baca-85bfb81f80e4
  Args:
    source: Prince_Henry
    type: :Person
  AssignClass (1cd984c8-e0ab-40ac-b5c1-29ee9a46571e)
 Call ID: 1cd984c8-e0ab-40ac-b5c1-29ee9a46571e
  Args:
    type: :Man
    source: Prince_George
  AssignClass (7e97b972-985f-4d08-88b0-bc43e1c5b9f7)
 Call ID: 7e97b972-985f-4d08-88b0-bc43e1c5b9f7
  Args:
    type: :Person
    source: Prince_George
  AddTriple (588ee022-e0f8-48b6-a288-1d4809088814)
 Call ID: 588ee022-e0f8-48b6-a288-1d4809088814
  Args:
    relation: :isSiblingOf
    target: Prince_Edward
    source: Prince_John
  AddTriple (866ea3bb-6ceb-4a88-875d-05ef98bb339e)
 Call ID: 866ea3bb-6ceb-4a88-875d-05ef98bb339e
  Args:
    source: Prince_John
    relation: :isSiblingOf
    target: Prince_Albert
  AddTriple (b42d3593-12ea-4474-b528-6d10d382a75e)
 Call ID: b42d3593-12ea-4474-b528-6d10d382a75e
  Args:
    source: Prince_John
    relation: :isSiblingOf
    target: Princess_Mary
  AddTriple (060bdb64-1ebd-4fc1-906c-438261b3ea20)
 Call ID: 060bdb64-1ebd-4fc1-906c-438261b3ea20
  Args:
    relation: :isSiblingOf
    target: Prince_Henry
    source: Prince_John
  AddTriple (b57c6536-3527-4843-9280-7d3b3941ca8e)
 Call ID: b57c6536-3527-4843-9280-7d3b3941ca8e
  Args:
    target: Prince_George
    relation: :isSiblingOf
    source: Prince_John
  Finish (07dddd07-c683-450f-8a79-445600c76aa7)
 Call ID: 07dddd07-c683-450f-8a79-445600c76aa7
  Args: