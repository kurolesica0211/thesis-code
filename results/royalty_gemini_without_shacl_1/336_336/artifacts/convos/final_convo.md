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
  AssignClass (3e234ede-2ecd-4021-95d2-b603ffc18af1)
 Call ID: 3e234ede-2ecd-4021-95d2-b603ffc18af1
  Args:
    type: :Woman
    source: Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (fb01f697-eff9-418b-be3f-70b7b404fd6b)
 Call ID: fb01f697-eff9-418b-be3f-70b7b404fd6b
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    type: :Person
  AddLiteral (3ea64597-7740-4e3b-9cf8-200170b34da5)
 Call ID: 3ea64597-7740-4e3b-9cf8-200170b34da5
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Alexandrine_of_Mecklenburg-Schwerin
    literal_value: 1879
  AddLiteral (994068e9-a04b-46f9-a807-db20bee43e6a)
 Call ID: 994068e9-a04b-46f9-a807-db20bee43e6a
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Alexandrine_of_Mecklenburg-Schwerin
    literal_value: 1952
  AssignClass (e87711eb-7713-420c-bff6-e8e0fdaec4f1)
 Call ID: e87711eb-7713-420c-bff6-e8e0fdaec4f1
  Args:
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
    type: :Man
  AssignClass (abb6327a-b829-4bce-8628-29a7fb54343c)
 Call ID: abb6327a-b829-4bce-8628-29a7fb54343c
  Args:
    type: :Person
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AssignClass (7bc2c0eb-6e22-4632-8cde-15b5155234ad)
 Call ID: 7bc2c0eb-6e22-4632-8cde-15b5155234ad
  Args:
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
    type: :Ancestor
  AssignClass (ca6f9352-af20-471b-969e-aff091960b66)
 Call ID: ca6f9352-af20-471b-969e-aff091960b66
  Args:
    type: :Woman
    source: Anastasia_Mikhailovna_of_Russia
  AssignClass (deb71f5c-df53-44ef-9073-83e63ccc9f1e)
 Call ID: deb71f5c-df53-44ef-9073-83e63ccc9f1e
  Args:
    source: Anastasia_Mikhailovna_of_Russia
    type: :Person
  AssignClass (7d1de5a6-9c4d-4f70-8e7f-ceb6e37606ec)
 Call ID: 7d1de5a6-9c4d-4f70-8e7f-ceb6e37606ec
  Args:
    type: :Ancestor
    source: Anastasia_Mikhailovna_of_Russia
  AddTriple (37a4d480-f548-4d0b-9211-d2d5792aa9f8)
 Call ID: 37a4d480-f548-4d0b-9211-d2d5792aa9f8
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasFather
    target: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AddTriple (f98672f9-a6c1-44d1-b7ee-931d9e6a07b7)
 Call ID: f98672f9-a6c1-44d1-b7ee-931d9e6a07b7
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasMother
    target: Anastasia_Mikhailovna_of_Russia
  AssignClass (e962d362-df36-4409-9b1d-b4de249bf0d0)
 Call ID: e962d362-df36-4409-9b1d-b4de249bf0d0
  Args:
    source: Christian_X_of_Denmark
    type: :Man
  AssignClass (dedcd9d3-84be-4531-97b3-99b118cd2ca4)
 Call ID: dedcd9d3-84be-4531-97b3-99b118cd2ca4
  Args:
    type: :Person
    source: Christian_X_of_Denmark
  AddTriple (de715c25-1acc-4eee-8b83-566df05360bf)
 Call ID: de715c25-1acc-4eee-8b83-566df05360bf
  Args:
    target: Christian_X_of_Denmark
    relation: :hasRelation
    source: Alexandrine_of_Mecklenburg-Schwerin
  AddLiteral (e8b26222-ad9c-4368-a9de-0f585dd39d86)
 Call ID: e8b26222-ad9c-4368-a9de-0f585dd39d86
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1898
  AssignClass (43eb91fe-1512-4802-95d4-5563167033e1)
 Call ID: 43eb91fe-1512-4802-95d4-5563167033e1
  Args:
    source: Frederick_Francis_IV_of_Mecklenburg-Schwerin
    type: :Man
  AssignClass (5bd044a3-57a0-425c-bbd2-f61129e6b39a)
 Call ID: 5bd044a3-57a0-425c-bbd2-f61129e6b39a
  Args:
    type: :Person
    source: Frederick_Francis_IV_of_Mecklenburg-Schwerin
  AddTriple (88f6bf2b-af3d-46ed-9613-0465a1d5f328)
 Call ID: 88f6bf2b-af3d-46ed-9613-0465a1d5f328
  Args:
    source: Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasBrother
    target: Frederick_Francis_IV_of_Mecklenburg-Schwerin
  AssignClass (13d5e67c-d50a-43ac-b87c-e7016872d3e7)
 Call ID: 13d5e67c-d50a-43ac-b87c-e7016872d3e7
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    type: :Woman
  AssignClass (07fe6e4b-98ec-48d4-94b5-2a1dd903473b)
 Call ID: 07fe6e4b-98ec-48d4-94b5-2a1dd903473b
  Args:
    type: :Person
    source: Cecilie_of_Mecklenburg-Schwerin
  AddTriple (72cc86c2-2b9b-474e-baec-ff5f657fee23)
 Call ID: 72cc86c2-2b9b-474e-baec-ff5f657fee23
  Args:
    target: Cecilie_of_Mecklenburg-Schwerin
    source: Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasSister
  Finish (22ca3a9a-02a6-4c08-a55a-eac714aabfb1)
 Call ID: 22ca3a9a-02a6-4c08-a55a-eac714aabfb1
  Args: