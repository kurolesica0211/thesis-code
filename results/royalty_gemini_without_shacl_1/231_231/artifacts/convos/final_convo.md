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
  AssignClass (1560bc7e-30b0-4db0-81ec-2dfc11881993)
 Call ID: 1560bc7e-30b0-4db0-81ec-2dfc11881993
  Args:
    source: Prince_John_of_the_United_Kingdom
    type: :Man
  AssignClass (0ae2fbcb-909a-42db-8b30-af70c55c9d1c)
 Call ID: 0ae2fbcb-909a-42db-8b30-af70c55c9d1c
  Args:
    type: :Person
    source: Prince_John_of_the_United_Kingdom
  AssignClass (c8ffa3c7-0fce-4c47-870e-9c3eac9531f7)
 Call ID: c8ffa3c7-0fce-4c47-870e-9c3eac9531f7
  Args:
    source: King_George_V
    type: :Ancestor
  AssignClass (d810deae-ec54-4d27-8d35-b81136ab4285)
 Call ID: d810deae-ec54-4d27-8d35-b81136ab4285
  Args:
    source: King_George_V
    type: :Man
  AssignClass (a39ae3d6-2320-436a-8883-83f4a16c4480)
 Call ID: a39ae3d6-2320-436a-8883-83f4a16c4480
  Args:
    type: :Person
    source: King_George_V
  AssignClass (958ecda8-431a-40d9-813a-9d69c7c44a02)
 Call ID: 958ecda8-431a-40d9-813a-9d69c7c44a02
  Args:
    type: :Ancestor
    source: Queen_Mary
  AssignClass (223b9e56-d233-43b4-afc3-d32f1221c6b6)
 Call ID: 223b9e56-d233-43b4-afc3-d32f1221c6b6
  Args:
    source: Queen_Mary
    type: :Woman
  AssignClass (955fdfd8-045f-43c8-b9b2-e0f3a3ffefb0)
 Call ID: 955fdfd8-045f-43c8-b9b2-e0f3a3ffefb0
  Args:
    source: Queen_Mary
    type: :Person
  AssignClass (af8decfc-f980-4572-96b6-37b25c500abd)
 Call ID: af8decfc-f980-4572-96b6-37b25c500abd
  Args:
    source: Edward_VII
    type: :Ancestor
  AssignClass (fabb4ef7-2e1c-4a63-8a96-1bcd28999191)
 Call ID: fabb4ef7-2e1c-4a63-8a96-1bcd28999191
  Args:
    type: :Man
    source: Edward_VII
  AssignClass (4ff17965-0127-40d5-955a-0892aecf6f54)
 Call ID: 4ff17965-0127-40d5-955a-0892aecf6f54
  Args:
    source: Edward_VII
    type: :Person
  AddTriple (3fee47e9-ffc5-45ff-82a7-567b4b1c8084)
 Call ID: 3fee47e9-ffc5-45ff-82a7-567b4b1c8084
  Args:
    relation: :hasFather
    target: King_George_V
    source: Prince_John_of_the_United_Kingdom
  AddTriple (99152612-c3cc-4463-b915-4ee8dc5b8139)
 Call ID: 99152612-c3cc-4463-b915-4ee8dc5b8139
  Args:
    relation: :hasMother
    target: Queen_Mary
    source: Prince_John_of_the_United_Kingdom
  AddTriple (8e53744d-aaad-430c-b00c-67ae033b6596)
 Call ID: 8e53744d-aaad-430c-b00c-67ae033b6596
  Args:
    relation: :hasFather
    source: King_George_V
    target: Edward_VII
  AddLiteral (f5ff0065-9faa-4540-9da6-ae10e6a7c7cd)
 Call ID: f5ff0065-9faa-4540-9da6-ae10e6a7c7cd
  Args:
    literal_value: 1905
    source: Prince_John_of_the_United_Kingdom
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (e181f7ef-23fd-49ba-88ce-4c52a10ca469)
 Call ID: e181f7ef-23fd-49ba-88ce-4c52a10ca469
  Args:
    literal_value: 1919
    source: Prince_John_of_the_United_Kingdom
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (df7ed47f-28c5-4fba-bd3b-26b00d42a2d9)
 Call ID: df7ed47f-28c5-4fba-bd3b-26b00d42a2d9
  Args:
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Johnnie
    source: Prince_John_of_the_United_Kingdom
  AssignClass (c30ae137-34d6-4aeb-a805-25ba14fad1de)
 Call ID: c30ae137-34d6-4aeb-a805-25ba14fad1de
  Args:
    type: :Man
    source: Prince_Edward
  AssignClass (28fa0aeb-698f-4649-86a6-b7f42531a7bc)
 Call ID: 28fa0aeb-698f-4649-86a6-b7f42531a7bc
  Args:
    source: Prince_Edward
    type: :Person
  AssignClass (2bce17f0-1fea-428d-a1ba-730875465a3b)
 Call ID: 2bce17f0-1fea-428d-a1ba-730875465a3b
  Args:
    type: :Man
    source: Prince_Albert
  AssignClass (653dc9dc-49bb-47bd-9efd-45045a2cc267)
 Call ID: 653dc9dc-49bb-47bd-9efd-45045a2cc267
  Args:
    source: Prince_Albert
    type: :Person
  AssignClass (3b52a642-e019-4043-bfa3-9fc917dcffb0)
 Call ID: 3b52a642-e019-4043-bfa3-9fc917dcffb0
  Args:
    source: Princess_Mary
    type: :Woman
  AssignClass (5ca5967f-52a1-4c8d-888b-94b9b990cb80)
 Call ID: 5ca5967f-52a1-4c8d-888b-94b9b990cb80
  Args:
    type: :Person
    source: Princess_Mary
  AssignClass (c7f5cf04-be44-401f-a6b9-5371faa8d08f)
 Call ID: c7f5cf04-be44-401f-a6b9-5371faa8d08f
  Args:
    type: :Man
    source: Prince_Henry
  AssignClass (ead89b32-68fe-4504-b09c-a2caaa1318c7)
 Call ID: ead89b32-68fe-4504-b09c-a2caaa1318c7
  Args:
    type: :Person
    source: Prince_Henry
  AssignClass (9fab7536-b49c-4dcb-82ae-e8e66dd69c4b)
 Call ID: 9fab7536-b49c-4dcb-82ae-e8e66dd69c4b
  Args:
    type: :Man
    source: Prince_George
  AssignClass (699dcd55-06eb-4e77-8f6b-353028bb9346)
 Call ID: 699dcd55-06eb-4e77-8f6b-353028bb9346
  Args:
    source: Prince_George
    type: :Person
  AddTriple (62526d25-fcaf-4405-b67a-7fbf805738d7)
 Call ID: 62526d25-fcaf-4405-b67a-7fbf805738d7
  Args:
    relation: :isSiblingOf
    source: Prince_John_of_the_United_Kingdom
    target: Prince_Edward
  AddTriple (17f786c0-9aa1-43ca-b85c-5d1a8ecdbbb5)
 Call ID: 17f786c0-9aa1-43ca-b85c-5d1a8ecdbbb5
  Args:
    source: Prince_John_of_the_United_Kingdom
    target: Prince_Albert
    relation: :isSiblingOf
  AddTriple (bf95fada-49bc-4801-9de4-06c8220d8dc8)
 Call ID: bf95fada-49bc-4801-9de4-06c8220d8dc8
  Args:
    relation: :isSiblingOf
    target: Princess_Mary
    source: Prince_John_of_the_United_Kingdom
  AddTriple (edc339dc-582c-4b6f-988e-6277fa9d8b03)
 Call ID: edc339dc-582c-4b6f-988e-6277fa9d8b03
  Args:
    source: Prince_John_of_the_United_Kingdom
    target: Prince_Henry
    relation: :isSiblingOf
  AddTriple (8374598e-896d-49b0-bf24-13e1d6f2d116)
 Call ID: 8374598e-896d-49b0-bf24-13e1d6f2d116
  Args:
    source: Prince_John_of_the_United_Kingdom
    target: Prince_George
    relation: :isSiblingOf
  Finish (90344120-5b85-46d8-bcce-998c8b9e6f2b)
 Call ID: 90344120-5b85-46d8-bcce-998c8b9e6f2b
  Args: