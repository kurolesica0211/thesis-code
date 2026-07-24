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
Alexandrine of Mecklenburg-Schwerin (Alexandrine Auguste; 24 December 1879 – 28 December 1952) was Queen of Denmark from 1912 to 1947, as well as Queen of Iceland from 1918 to 1944 as the wife of King Christian X.


Alexandrine was the daughter of Frederick Francis III, Grand Duke of Mecklenburg-Schwerin, and Grand Duchess Anastasia Mikhailovna of Russia.
She was brought up with simplicity, and her early life was peripatetic, spending summers in Mecklenburg and the rest of the year in the south of France.
She married Prince Christian of Denmark in 1898.
Alexandrine became crown princess in 1906 and queen consort of Denmark in 1912.
Early life

Birth and family

Alexandrine was born a Duchess of Mecklenburg-Schwerin on Christmas Eve of 1879, in the city of Schwerin, the capital of the vast Grand Duchy of Mecklenburg-Schwerin in Northern Germany.
Her father was Frederick Francis, Hereditary Grand Duke of Mecklenburg-Schwerin; who was the eldest son of and heir to the reigning Grand Duke Frederick Francis II.
Her mother was Grand Duchess Anastasia Mikhailovna of Russia, who was a granddaughter of Emperor Nicholas I of Russia.
Alexandrine was her parents' first child, and was born eleven months after their wedding in St. Petersburg.
She was born in the Neustadt Palace (New Town Palace) in Schwerin, which was her parents' residence in the city at the time.
Duchess Alexandrine had two younger siblings: her only brother was Duke Frederick Francis, who in 1897 succeeded their father as Grand Duke of Mecklenburg-Schwerin, and her only sister was Duchess Cecilie, who in 1906 married the German Crown Prince Wilhelm of Prussia, eldest son of German Emperor William II.
Her mother was the paternal aunt of Princess Irina Alexandrovna of Russia, the wife of Felix Yusupov, one of the murderers of Rasputin.
Childhood and early adulthood

After their father's succession as Grand Duke upon the death of his father on 15 April 1883, Alexandrine grew up with her brother and sister at the Castle in Schwerin, at the royal residences of Ludwigslust Palace and the Gelbensande hunting lodge, only a few kilometres from the Baltic Sea coast.
The wet, damp, and cold Northern European climate of Mecklenburg was not good for his health, and as a result, Alexandrine spent a large amount of time with her family away from Mecklenburg, by the Lake Geneva, and in Palermo, Baden-Baden and Cannes in the south of France, where the family owned a large estate, the Villa Wenden.
Cannes was favoured at the time by European royalty, including some whom Alexandrine personally met, such as Empress Eugénie of France and her future husband's uncle, Edward VII of the United Kingdom.
First years in Denmark

Engagement and marriage

It was also in Cannes during the winter visit of 1897 that Duchess Alexandrine met her future husband, Prince Christian of Denmark, the eldest son of Crown Prince Frederik and Crown Princess Louise of Denmark.
The two young royals were engaged in Schwerin on 24 March 1897.
In April 1897, shortly after the engagement was announced, her father the Grand Duke died suddenly at the age of just 46 years.
The wedding of Duchess Alexandrine and Prince Christian was celebrated on 26 April 1898 in Cannes, when she was 18 years old.
They had two children:


Early years in Denmark

Upon their arrival in Denmark, the couple were given Christian VIII's Palace at the Amalienborg palace complex in central Copenhagen as their principal residence and Sorgenfri Palace in Kongens Lyngby north of Copenhagen as a summer residence.
On 29 January 1906, her husband's grandfather King Christian IX died, and Christian's father ascended the throne as King Frederik VIII.
Christian himself became crown prince, and Alexandrine became crown princess.
Alexandrine's husband acceded to the throne as Christian X, and Alexandrine became queen consort of Denmark.
The revolution in Russia brought much heartbreak for Alexandrine as three of her uncles, Nicholas, George and Sergey, were killed by the Bolsheviks.
Her rejection of Major General Kurt Himer, Chief of Staff to General Kaupisch on 9 April 1940 became a symbol for her loyalty toward Denmark before her birth country Germany and was diplomatically obliged to receive the German General commander at her castle.
When General Himer asked for an audience with the monarch, Christian was persuaded to receive him by his daughter-in-law as he would any other, which was supported by Alexandrine.
He asked to do so alone, but Alexandrine told him she would interrupt them.
"


It was reported, that although Alexandrine was seen as shy and disliked official ceremonies, she had a "sharp" intelligence, and she was, together with her daughter-in-law, Ingrid of Sweden, a true support of the monarch and a driving force for the resistance toward the occupation within the royal house.
It was also reported, that in contrast to the monarch himself and the Crown Prince, the Queen and the Crown Princess never lost their calm when the nation was attacked.
Her first years in Denmark were afflicted by the prevailing anti-German attitude of the Danes, but she won them over.
Kaj Munk is quoted to describe the public appreciation of her during World War II with his comment: "Protect our Queen, the only German we would like to keep!"


Later life

In 1947, she was widowed; she became the first queen dowager of Denmark to opt not to use that title.
In her later years, Alexandrine spent most of her widowhood at Marselisborg Castle in Jutland.
Queen Alexandrine died on 28 December 1952 in her sleep, four days after her birthday.



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
  AssignClass (f1368219-26ef-464d-9caf-3189f11bdadd)
 Call ID: f1368219-26ef-464d-9caf-3189f11bdadd
  Args:
    type: :Woman
    source: Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (2cda7ff9-e97b-4f11-aa72-9e8d25fc0b68)
 Call ID: 2cda7ff9-e97b-4f11-aa72-9e8d25fc0b68
  Args:
    type: :Person
    source: Alexandrine_of_Mecklenburg-Schwerin
  AddLiteral (08268412-fc62-48b6-95fe-7e1a6d5651d5)
 Call ID: 08268412-fc62-48b6-95fe-7e1a6d5651d5
  Args:
    literal_type: xsd:integer
    literal_value: 1879
    relation: :hasBirthYear
    source: Alexandrine_of_Mecklenburg-Schwerin
  AddLiteral (f165d58f-0324-4b80-98bc-d359928cf8d7)
 Call ID: f165d58f-0324-4b80-98bc-d359928cf8d7
  Args:
    relation: :hasDeathYear
    source: Alexandrine_of_Mecklenburg-Schwerin
    literal_value: 1952
    literal_type: xsd:integer
  AssignClass (9a1cbd03-bb4e-44f2-9dcf-96211a56c0fc)
 Call ID: 9a1cbd03-bb4e-44f2-9dcf-96211a56c0fc
  Args:
    type: :Man
    source: Frederick_Francis_III
  AssignClass (2469e05c-5759-4eee-9246-af1d88eda419)
 Call ID: 2469e05c-5759-4eee-9246-af1d88eda419
  Args:
    type: :Ancestor
    source: Frederick_Francis_III
  AssignClass (a31a954f-d425-4dc5-a6c3-5e355bcb964b)
 Call ID: a31a954f-d425-4dc5-a6c3-5e355bcb964b
  Args:
    type: :Person
    source: Frederick_Francis_III
  AssignClass (36221f93-7293-4d79-b4bc-78614788cea3)
 Call ID: 36221f93-7293-4d79-b4bc-78614788cea3
  Args:
    source: Anastasia_Mikhailovna
    type: :Woman
  AssignClass (522fdbad-9225-493e-b7c3-bd078e8aaf62)
 Call ID: 522fdbad-9225-493e-b7c3-bd078e8aaf62
  Args:
    type: :Ancestor
    source: Anastasia_Mikhailovna
  AssignClass (da115bf4-3fdb-425f-9412-6b9be0b8df95)
 Call ID: da115bf4-3fdb-425f-9412-6b9be0b8df95
  Args:
    type: :Person
    source: Anastasia_Mikhailovna
  AddTriple (fb91ddfb-b1bd-4908-ad18-0715cb8ab1d8)
 Call ID: fb91ddfb-b1bd-4908-ad18-0715cb8ab1d8
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasFather
    target: Frederick_Francis_III
  AddTriple (84bb65da-9499-4e0a-baab-fc578d7bad32)
 Call ID: 84bb65da-9499-4e0a-baab-fc578d7bad32
  Args:
    target: Anastasia_Mikhailovna
    source: Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasMother
  AssignClass (d9549396-a77c-4e8c-98bd-5983a4833262)
 Call ID: d9549396-a77c-4e8c-98bd-5983a4833262
  Args:
    type: :Man
    source: Christian_X
  AssignClass (c49be875-2aec-42b8-aef3-4380dd461cbc)
 Call ID: c49be875-2aec-42b8-aef3-4380dd461cbc
  Args:
    type: :Person
    source: Christian_X
  AddLiteral (b3743c61-3878-4fd0-a95a-db3a0b5e1781)
 Call ID: b3743c61-3878-4fd0-a95a-db3a0b5e1781
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1898
  AddTriple (fd8e8ca3-c053-4d0d-af93-429be0ee7338)
 Call ID: fd8e8ca3-c053-4d0d-af93-429be0ee7338
  Args:
    target: Christian_X
    relation: :hasRelation
    source: Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (db59892b-d1c7-4a96-bb70-0472476b2a4d)
 Call ID: db59892b-d1c7-4a96-bb70-0472476b2a4d
  Args:
    type: :Man
    source: Duke_Frederick_Francis
  AssignClass (64fbd6ed-5e08-457c-8eb3-294570946f23)
 Call ID: 64fbd6ed-5e08-457c-8eb3-294570946f23
  Args:
    type: :Person
    source: Duke_Frederick_Francis
  AddTriple (a8a9c916-20ea-42a0-9890-36340f6407c0)
 Call ID: a8a9c916-20ea-42a0-9890-36340f6407c0
  Args:
    target: Duke_Frederick_Francis
    source: Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasBrother
  AssignClass (34ecadb1-9731-4221-b2f5-6decf8367a5a)
 Call ID: 34ecadb1-9731-4221-b2f5-6decf8367a5a
  Args:
    source: Duchess_Cecilie
    type: :Woman
  AssignClass (1a546e95-48f6-49f6-aecf-ed2ce9d9fe46)
 Call ID: 1a546e95-48f6-49f6-aecf-ed2ce9d9fe46
  Args:
    source: Duchess_Cecilie
    type: :Person
  AddTriple (b5c2c6d8-c650-4288-b722-babe7daf8c71)
 Call ID: b5c2c6d8-c650-4288-b722-babe7daf8c71
  Args:
    target: Duchess_Cecilie
    relation: :hasSister
    source: Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (b29e15b4-944a-4a98-a995-20673e7b46f0)
 Call ID: b29e15b4-944a-4a98-a995-20673e7b46f0
  Args:
    source: Frederick_Francis_II
    type: :Man
  AssignClass (df762bab-d133-409a-ae10-d100b24a7a98)
 Call ID: df762bab-d133-409a-ae10-d100b24a7a98
  Args:
    type: :Ancestor
    source: Frederick_Francis_II
  AssignClass (3931d864-cc24-45c0-b86c-17ad58a82f0d)
 Call ID: 3931d864-cc24-45c0-b86c-17ad58a82f0d
  Args:
    type: :Person
    source: Frederick_Francis_II
  AddTriple (cbc7f917-646d-4350-b7ee-463f4160a0a5)
 Call ID: cbc7f917-646d-4350-b7ee-463f4160a0a5
  Args:
    target: Frederick_Francis_II
    relation: :hasFather
    source: Frederick_Francis_III
  AssignClass (ef290839-df06-43ab-8092-f08d5eb730ef)
 Call ID: ef290839-df06-43ab-8092-f08d5eb730ef
  Args:
    source: Nicholas_I_of_Russia
    type: :Man
  AssignClass (c47ffbf5-beae-418a-8a0c-fbce27a2fce0)
 Call ID: c47ffbf5-beae-418a-8a0c-fbce27a2fce0
  Args:
    source: Nicholas_I_of_Russia
    type: :Ancestor
  AssignClass (938b8184-a59a-4353-9fcd-8dded51b8b1e)
 Call ID: 938b8184-a59a-4353-9fcd-8dded51b8b1e
  Args:
    source: Nicholas_I_of_Russia
    type: :Person
  AddTriple (6d1ad087-db39-4f1f-9944-0a73f71d0ffd)
 Call ID: 6d1ad087-db39-4f1f-9944-0a73f71d0ffd
  Args:
    source: Nicholas_I_of_Russia
    relation: :isAncestorOf
    target: Anastasia_Mikhailovna
  AssignClass (13987e7c-c6ab-45fc-b01f-d9bbe7c089c8)
 Call ID: 13987e7c-c6ab-45fc-b01f-d9bbe7c089c8
  Args:
    type: :Man
    source: Frederik_VIII
  AssignClass (6d02db05-357a-4794-9dc5-a78d1a8be98a)
 Call ID: 6d02db05-357a-4794-9dc5-a78d1a8be98a
  Args:
    type: :Ancestor
    source: Frederik_VIII
  AssignClass (6b59f322-ddcd-4415-ba1c-7e9c988a4902)
 Call ID: 6b59f322-ddcd-4415-ba1c-7e9c988a4902
  Args:
    type: :Person
    source: Frederik_VIII
  AssignClass (3ecb6a59-c983-4a7c-a78c-bf045615437c)
 Call ID: 3ecb6a59-c983-4a7c-a78c-bf045615437c
  Args:
    source: Louise_of_Denmark
    type: :Woman
  AssignClass (b97983f2-f6ab-423c-bff7-7e6707578706)
 Call ID: b97983f2-f6ab-423c-bff7-7e6707578706
  Args:
    source: Louise_of_Denmark
    type: :Ancestor
  AssignClass (f8a93fd2-7d12-49e8-9ddd-536f582be4c4)
 Call ID: f8a93fd2-7d12-49e8-9ddd-536f582be4c4
  Args:
    type: :Person
    source: Louise_of_Denmark
  AddTriple (e2f8de92-f21a-4017-bc96-ea865b77143d)
 Call ID: e2f8de92-f21a-4017-bc96-ea865b77143d
  Args:
    source: Christian_X
    relation: :hasFather
    target: Frederik_VIII
  AddTriple (03d8b70e-3dd2-4b52-9a51-62666b3f4da0)
 Call ID: 03d8b70e-3dd2-4b52-9a51-62666b3f4da0
  Args:
    relation: :hasMother
    source: Christian_X
    target: Louise_of_Denmark
  AssignClass (ac4bd8cf-5da1-4a15-b872-34324b5fff76)
 Call ID: ac4bd8cf-5da1-4a15-b872-34324b5fff76
  Args:
    source: Christian_IX
    type: :Man
  AssignClass (07566325-1a48-4f96-af75-bbd088245d91)
 Call ID: 07566325-1a48-4f96-af75-bbd088245d91
  Args:
    source: Christian_IX
    type: :Ancestor
  AssignClass (89467a30-26a2-4c97-9ddf-092b45f0b675)
 Call ID: 89467a30-26a2-4c97-9ddf-092b45f0b675
  Args:
    type: :Person
    source: Christian_IX
  AddTriple (1eb5cfb0-729c-4e70-906b-4abb30a01316)
 Call ID: 1eb5cfb0-729c-4e70-906b-4abb30a01316
  Args:
    target: Christian_IX
    source: Frederik_VIII
    relation: :hasFather
  AssignClass (6158a21b-206a-422d-9801-b2d2242d808c)
 Call ID: 6158a21b-206a-422d-9801-b2d2242d808c
  Args:
    source: Wilhelm_of_Prussia
    type: :Man
  AssignClass (1cf3192c-9139-48f1-a574-1312ab3eb814)
 Call ID: 1cf3192c-9139-48f1-a574-1312ab3eb814
  Args:
    type: :Person
    source: Wilhelm_of_Prussia
  AddTriple (7053c737-0857-4178-bc51-32fa8d961ec8)
 Call ID: 7053c737-0857-4178-bc51-32fa8d961ec8
  Args:
    target: Wilhelm_of_Prussia
    relation: :hasRelation
    source: Duchess_Cecilie
  AssignClass (ccc9b9c8-060d-4632-8753-2285862d0d44)
 Call ID: ccc9b9c8-060d-4632-8753-2285862d0d44
  Args:
    source: William_II_of_Germany
    type: :Man
  AssignClass (cb0cbf53-e8fe-4f93-8a23-cca9ebf6c283)
 Call ID: cb0cbf53-e8fe-4f93-8a23-cca9ebf6c283
  Args:
    source: William_II_of_Germany
    type: :Ancestor
  AssignClass (66d0cd2c-3547-4e18-8f22-12b91ecfbd4e)
 Call ID: 66d0cd2c-3547-4e18-8f22-12b91ecfbd4e
  Args:
    type: :Person
    source: William_II_of_Germany
  AddTriple (8a9ce8b2-c060-4ae2-90dd-a99249ebecee)
 Call ID: 8a9ce8b2-c060-4ae2-90dd-a99249ebecee
  Args:
    relation: :hasFather
    source: Wilhelm_of_Prussia
    target: William_II_of_Germany
  AssignClass (127cd200-d03a-430a-a536-b21965113a01)
 Call ID: 127cd200-d03a-430a-a536-b21965113a01
  Args:
    type: :Woman
    source: Ingrid_of_Sweden
  AssignClass (da370197-802e-4615-acdc-69f84199e685)
 Call ID: da370197-802e-4615-acdc-69f84199e685
  Args:
    source: Ingrid_of_Sweden
    type: :Person
  AddTriple (0e9be367-8305-40f9-aab9-f85e3ad0b9b1)
 Call ID: 0e9be367-8305-40f9-aab9-f85e3ad0b9b1
  Args:
    target: Christian_X
    relation: :hasRelation
    source: Ingrid_of_Sweden
  Finish (845ff1df-a052-4189-bef3-17ae08eee02f)
 Call ID: 845ff1df-a052-4189-bef3-17ae08eee02f
  Args: