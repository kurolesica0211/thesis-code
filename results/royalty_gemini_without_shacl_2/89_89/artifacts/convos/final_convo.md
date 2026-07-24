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
Prince Nicholas of Greece and Denmark (Greek: Νικόλαος, romanized: Nikólaos; 22 January 1872 – 8 February 1938) was the fourth child and third son of King George I of Greece, and of Queen Olga.
He was known as "Greek Nicky" within the family to distinguish him from his cousin Emperor Nicholas II of Russia (first cousin on the paternal side and second cousin on the maternal side).
Prince Nicholas was a talented painter, often signing his works as "Nicolas Leprince".
Marriage and issue

He married Grand Duchess Elena Vladimirovna of Russia (1882–1957), daughter of Grand Duke Vladimir Alexandrovich of Russia and Marie of Mecklenburg-Schwerin, the only sister of the future Russian imperial pretender, Grand Duke Kirill Vladimirovich, and his second cousin through his mother Olga Constantinovna of Russia and her father Grand Duke Vladimir Alexandrovich of Russia, on 29 August 1902 in Tsarskoye Selo, Russia.
Residence in Athens

Nicholas' marriage significantly improved his own financial position; his wife Elena received the customary imperial dowry of a Russian Grand Duchess, amounting to 1,000,000 roubles.
The dowry capital was held in Russia, from which Elena was paid an annual income of 50,000 roubles.
After their marriage the couple resided in Athens; in late 1902 they purchased a large house near the city centre, which was thereafter known as the Nicholas Palace.
Prince and Princess Nicholas took up residence at the newly-renovated Nicholas Palace in 1904.
The advent of the Russian Revolution in 1917 and the exile of the Greek Royal Family in 1923 had a significant impact on the couple's income, and as a result the Nicholas Palace was leased to the Hotel Grande Bretagne during the 1920s, who used the building as a 60-bed luxury annex known as the “Petit Palais”.
The Italian Government later purchased the Nicholas Palace from the widowed Princess Nicholas in 1955; the site has subsequently remained the home of the Italian Embassy in Athens ever since.
Public life

Along with his elder brothers Constantine and George, Nicholas helped to organize the 1896 Summer Olympics in Athens, the first to be held since 393.
Nicholas served as president of the Sub-Committee for Shooting.
His father bequeathed him the Royal Theater of Greece which Nicholas, in turn, transferred to the Greek state in 1935.
He was friends with George Simitis and was godfather to his son, future socialist Prime Minister Kostas Simitis.
Death and burial

Prince Nicholas died in Athens on February 8, 1938 and was buried in the Royal tomb at the Palace of Tatoi.



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
  AssignClass (abd6034e-cb01-4e45-acea-d2662fe682dd)
 Call ID: abd6034e-cb01-4e45-acea-d2662fe682dd
  Args:
    type: :Man
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (82e4e2db-5f8f-4386-a562-8313051c55c1)
 Call ID: 82e4e2db-5f8f-4386-a562-8313051c55c1
  Args:
    type: :Person
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (f10627d1-4850-4ad7-a1c9-0d15c46779de)
 Call ID: f10627d1-4850-4ad7-a1c9-0d15c46779de
  Args:
    type: :Man
    source: King_George_I_of_Greece
  AssignClass (b298858d-e5ad-4c4d-942a-646c4f1dce04)
 Call ID: b298858d-e5ad-4c4d-942a-646c4f1dce04
  Args:
    source: King_George_I_of_Greece
    type: :Person
  AssignClass (4c1e86cf-c6c0-4987-9a89-7def57a9001b)
 Call ID: 4c1e86cf-c6c0-4987-9a89-7def57a9001b
  Args:
    type: :Woman
    source: Queen_Olga
  AssignClass (1cd2deeb-3d3b-4b06-b386-bc4a4f3906ae)
 Call ID: 1cd2deeb-3d3b-4b06-b386-bc4a4f3906ae
  Args:
    type: :Person
    source: Queen_Olga
  AddLiteral (2487f9c1-1bf1-49cf-a679-4403c6498c21)
 Call ID: 2487f9c1-1bf1-49cf-a679-4403c6498c21
  Args:
    literal_value: 1872
    relation: :hasBirthYear
    source: Prince_Nicholas_of_Greece_and_Denmark
    literal_type: xsd:integer
  AddLiteral (b5647610-47a0-430c-a8f1-ade24b6856b6)
 Call ID: b5647610-47a0-430c-a8f1-ade24b6856b6
  Args:
    relation: :hasDeathYear
    literal_value: 1938
    literal_type: xsd:integer
    source: Prince_Nicholas_of_Greece_and_Denmark
  AddTriple (aad8324e-0395-4cf1-806d-84edeaf5b475)
 Call ID: aad8324e-0395-4cf1-806d-84edeaf5b475
  Args:
    target: King_George_I_of_Greece
    source: Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasFather
  AddTriple (3c4ad90e-5e0a-4385-8dc3-b5e32d9389af)
 Call ID: 3c4ad90e-5e0a-4385-8dc3-b5e32d9389af
  Args:
    target: Queen_Olga
    source: Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasMother
  AddLiteral (1f8b4332-0c83-4ac5-b092-69688a287bd2)
 Call ID: 1f8b4332-0c83-4ac5-b092-69688a287bd2
  Args:
    literal_type: xsd:string
    source: Prince_Nicholas_of_Greece_and_Denmark
    relation: :knownAs
    literal_value: Greek Nicky
  AddLiteral (b823ce45-9bf9-488f-8e43-0830caa40422)
 Call ID: b823ce45-9bf9-488f-8e43-0830caa40422
  Args:
    relation: :alsoKnownAs
    literal_value: Nicolas Leprince
    source: Prince_Nicholas_of_Greece_and_Denmark
    literal_type: xsd:string
  AssignClass (3dac6de5-eb68-4152-b806-17c02a7088b6)
 Call ID: 3dac6de5-eb68-4152-b806-17c02a7088b6
  Args:
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    type: :Woman
  AssignClass (10a563f4-2f38-4a79-853b-aaacd2d43bf8)
 Call ID: 10a563f4-2f38-4a79-853b-aaacd2d43bf8
  Args:
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    type: :Person
  AddTriple (5f726774-3e11-4bdc-b69d-5895e51ab964)
 Call ID: 5f726774-3e11-4bdc-b69d-5895e51ab964
  Args:
    relation: :hasRelation
    source: Prince_Nicholas_of_Greece_and_Denmark
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AddLiteral (56d0e2fc-2125-4a1c-9709-7f6732964155)
 Call ID: 56d0e2fc-2125-4a1c-9709-7f6732964155
  Args:
    relation: :hasMarriageYear
    literal_value: 1902
    source: Prince_Nicholas_of_Greece_and_Denmark
    literal_type: xsd:integer
  AssignClass (6c513f2a-e0ac-4913-8753-d0dec964a3c4)
 Call ID: 6c513f2a-e0ac-4913-8753-d0dec964a3c4
  Args:
    source: Grand_Duke_Vladimir_Alexandrovich_of_Russia
    type: :Man
  AssignClass (33e2b1ab-b378-4684-a64f-399c82d31c7c)
 Call ID: 33e2b1ab-b378-4684-a64f-399c82d31c7c
  Args:
    source: Grand_Duke_Vladimir_Alexandrovich_of_Russia
    type: :Person
  AssignClass (38a75657-b56b-4041-a38c-105a295f97fa)
 Call ID: 38a75657-b56b-4041-a38c-105a295f97fa
  Args:
    type: :Woman
    source: Marie_of_Mecklenburg-Schwerin
  AssignClass (6aba2a1c-5ddf-4fec-80f8-2e820a6ed7fb)
 Call ID: 6aba2a1c-5ddf-4fec-80f8-2e820a6ed7fb
  Args:
    type: :Person
    source: Marie_of_Mecklenburg-Schwerin
  AddTriple (1ad80e20-ca8d-4405-9ec1-db6a49acc50a)
 Call ID: 1ad80e20-ca8d-4405-9ec1-db6a49acc50a
  Args:
    relation: :hasFather
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    target: Grand_Duke_Vladimir_Alexandrovich_of_Russia
  AddTriple (20bd29f9-e006-45af-bc10-fb634f8203fa)
 Call ID: 20bd29f9-e006-45af-bc10-fb634f8203fa
  Args:
    relation: :hasMother
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    target: Marie_of_Mecklenburg-Schwerin
  AssignClass (a8495744-78d0-4c40-beea-77a2a0f4e51e)
 Call ID: a8495744-78d0-4c40-beea-77a2a0f4e51e
  Args:
    source: Grand_Duke_Kirill_Vladimirovich
    type: :Man
  AssignClass (46780a7b-5779-4eca-8725-0368eeabad74)
 Call ID: 46780a7b-5779-4eca-8725-0368eeabad74
  Args:
    type: :Person
    source: Grand_Duke_Kirill_Vladimirovich
  AddTriple (fca27e36-b011-437e-a35a-e8b49fbdbd62)
 Call ID: fca27e36-b011-437e-a35a-e8b49fbdbd62
  Args:
    relation: :isSiblingOf
    target: Grand_Duke_Kirill_Vladimirovich
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (a72a8757-0fb6-4719-b3d2-fb079d682874)
 Call ID: a72a8757-0fb6-4719-b3d2-fb079d682874
  Args:
    type: :Man
    source: Constantine
  AssignClass (efe00ec7-ce04-4208-ab91-314c65d5392b)
 Call ID: efe00ec7-ce04-4208-ab91-314c65d5392b
  Args:
    type: :Person
    source: Constantine
  AssignClass (62954ae4-615f-4dd3-b191-86a0cc49085f)
 Call ID: 62954ae4-615f-4dd3-b191-86a0cc49085f
  Args:
    type: :Man
    source: George
  AssignClass (17d8ea66-e8e7-4e9c-abd7-3a154766e5d9)
 Call ID: 17d8ea66-e8e7-4e9c-abd7-3a154766e5d9
  Args:
    source: George
    type: :Person
  AddTriple (75dc8645-fed0-43fc-bb3d-7ef5dada7fce)
 Call ID: 75dc8645-fed0-43fc-bb3d-7ef5dada7fce
  Args:
    relation: :isSiblingOf
    source: Prince_Nicholas_of_Greece_and_Denmark
    target: Constantine
  AddTriple (5eb22ac3-4877-4622-bce6-833aefe359c4)
 Call ID: 5eb22ac3-4877-4622-bce6-833aefe359c4
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    target: George
    relation: :isSiblingOf
  AssignClass (1b7128df-809d-41ce-ba3c-bc6a1912d71b)
 Call ID: 1b7128df-809d-41ce-ba3c-bc6a1912d71b
  Args:
    source: Emperor_Nicholas_II_of_Russia
    type: :Man
  AssignClass (df4bff97-d8d8-4a73-bb93-f3c27f0614b4)
 Call ID: df4bff97-d8d8-4a73-bb93-f3c27f0614b4
  Args:
    source: Emperor_Nicholas_II_of_Russia
    type: :Person
  AddTriple (3d1b5fee-76b7-451a-ad32-edb3fa20a5f2)
 Call ID: 3d1b5fee-76b7-451a-ad32-edb3fa20a5f2
  Args:
    relation: :isBloodrelationOf
    source: Prince_Nicholas_of_Greece_and_Denmark
    target: Emperor_Nicholas_II_of_Russia
  AssignClass (a6af8259-71a5-4d61-902b-f29d8d4148b0)
 Call ID: a6af8259-71a5-4d61-902b-f29d8d4148b0
  Args:
    type: :Man
    source: George_Simitis
  AssignClass (64d0dd84-480d-4b5b-b1a7-f86ee61ad6b8)
 Call ID: 64d0dd84-480d-4b5b-b1a7-f86ee61ad6b8
  Args:
    source: George_Simitis
    type: :Person
  AddTriple (0e273d18-d072-4904-b04c-fab24407f66b)
 Call ID: 0e273d18-d072-4904-b04c-fab24407f66b
  Args:
    relation: :hasRelation
    target: George_Simitis
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (0d0df165-2521-41a5-b2c0-0a992ca47cd6)
 Call ID: 0d0df165-2521-41a5-b2c0-0a992ca47cd6
  Args:
    type: :Man
    source: Kostas_Simitis
  AssignClass (e6e40fec-4155-4663-9322-6ed90425482f)
 Call ID: e6e40fec-4155-4663-9322-6ed90425482f
  Args:
    type: :Person
    source: Kostas_Simitis
  AddTriple (48ef0b0f-78a8-4c04-b9dc-e73a9ea56edf)
 Call ID: 48ef0b0f-78a8-4c04-b9dc-e73a9ea56edf
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    target: Kostas_Simitis
    relation: :hasRelation
  Finish (9635c946-7a0c-4898-ba83-c81efeeb0d1b)
 Call ID: 9635c946-7a0c-4898-ba83-c81efeeb0d1b
  Args: