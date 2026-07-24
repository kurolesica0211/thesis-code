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
  AssignClass (76de5c64-2b38-4b81-9ec9-03c29f43f85e)
 Call ID: 76de5c64-2b38-4b81-9ec9-03c29f43f85e
  Args:
    type: :Man
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (c14ae4da-7b90-4ef8-8acb-f7ac78eef26f)
 Call ID: c14ae4da-7b90-4ef8-8acb-f7ac78eef26f
  Args:
    type: :Person
    source: Prince_Nicholas_of_Greece_and_Denmark
  AddLiteral (410a91c8-9bfb-46bd-947b-deb0fb28a7db)
 Call ID: 410a91c8-9bfb-46bd-947b-deb0fb28a7db
  Args:
    literal_type: xsd:integer
    source: Prince_Nicholas_of_Greece_and_Denmark
    literal_value: 1872
    relation: :hasBirthYear
  AddLiteral (5c6fc194-f14b-47be-8fd1-f4f53b082104)
 Call ID: 5c6fc194-f14b-47be-8fd1-f4f53b082104
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Prince_Nicholas_of_Greece_and_Denmark
    literal_value: 1938
  AddLiteral (ddca122a-85a0-4a7c-9ae7-85330f82092c)
 Call ID: ddca122a-85a0-4a7c-9ae7-85330f82092c
  Args:
    relation: :knownAs
    literal_value: Greek Nicky
    literal_type: xsd:string
    source: Prince_Nicholas_of_Greece_and_Denmark
  AddLiteral (4c4d42e4-37ab-4d96-946c-7eb62ae8fa8c)
 Call ID: 4c4d42e4-37ab-4d96-946c-7eb62ae8fa8c
  Args:
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: Prince_Nicholas_of_Greece_and_Denmark
    literal_value: Nicolas Leprince
  AssignClass (6a9f66bc-8d56-4cb8-b3ef-6a19b7682e73)
 Call ID: 6a9f66bc-8d56-4cb8-b3ef-6a19b7682e73
  Args:
    source: King_George_I_of_Greece
    type: :Man
  AssignClass (24e29850-7be5-4d7e-8e1d-d9b252939c4f)
 Call ID: 24e29850-7be5-4d7e-8e1d-d9b252939c4f
  Args:
    source: King_George_I_of_Greece
    type: :Person
  AddTriple (ca6e5941-9dba-4567-8972-eed30f43c299)
 Call ID: ca6e5941-9dba-4567-8972-eed30f43c299
  Args:
    relation: :isFatherOf
    source: King_George_I_of_Greece
    target: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (1e9b1194-fc7f-4f1b-ab2f-3cd6e5ec04fe)
 Call ID: 1e9b1194-fc7f-4f1b-ab2f-3cd6e5ec04fe
  Args:
    type: :Woman
    source: Queen_Olga
  AssignClass (d7157240-f8e4-4e7f-a74c-ecca2ca5ead3)
 Call ID: d7157240-f8e4-4e7f-a74c-ecca2ca5ead3
  Args:
    type: :Person
    source: Queen_Olga
  AddTriple (24b85376-2055-463f-99ff-47b3d50d5b2d)
 Call ID: 24b85376-2055-463f-99ff-47b3d50d5b2d
  Args:
    source: Queen_Olga
    target: Prince_Nicholas_of_Greece_and_Denmark
    relation: :isMotherOf
  AssignClass (1c2d9baf-c27f-4a88-9014-cb63b80d603c)
 Call ID: 1c2d9baf-c27f-4a88-9014-cb63b80d603c
  Args:
    type: :Woman
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (d9f15b46-a000-4f69-aa5f-feeb759fba7d)
 Call ID: d9f15b46-a000-4f69-aa5f-feeb759fba7d
  Args:
    type: :Person
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AddLiteral (b81096dc-dbc8-4b96-bd86-45e03fc86ece)
 Call ID: b81096dc-dbc8-4b96-bd86-45e03fc86ece
  Args:
    literal_type: xsd:integer
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    literal_value: 1882
    relation: :hasBirthYear
  AddLiteral (eef414fb-e9e9-42c5-aece-b0aba2061b8a)
 Call ID: eef414fb-e9e9-42c5-aece-b0aba2061b8a
  Args:
    relation: :hasDeathYear
    literal_value: 1957
    literal_type: xsd:integer
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AddLiteral (40c09929-1de3-4016-acdb-9b834f581942)
 Call ID: 40c09929-1de3-4016-acdb-9b834f581942
  Args:
    literal_type: xsd:integer
    source: Prince_Nicholas_of_Greece_and_Denmark
    literal_value: 1902
    relation: :hasMarriageYear
  AssignClass (dad85dbc-916d-4fdb-af81-765835e66dae)
 Call ID: dad85dbc-916d-4fdb-af81-765835e66dae
  Args:
    source: Grand_Duke_Vladimir_Alexandrovich_of_Russia
    type: :Man
  AssignClass (c8fe5cc1-7e2c-41ab-b821-7f8b64d639ea)
 Call ID: c8fe5cc1-7e2c-41ab-b821-7f8b64d639ea
  Args:
    type: :Person
    source: Grand_Duke_Vladimir_Alexandrovich_of_Russia
  AddTriple (58ac3d10-1dc2-4528-9fda-42a45ab6669d)
 Call ID: 58ac3d10-1dc2-4528-9fda-42a45ab6669d
  Args:
    relation: :isFatherOf
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
    source: Grand_Duke_Vladimir_Alexandrovich_of_Russia
  AssignClass (4225405a-066b-4367-bcbd-bd7ade125233)
 Call ID: 4225405a-066b-4367-bcbd-bd7ade125233
  Args:
    source: Marie_of_Mecklenburg-Schwerin
    type: :Woman
  AssignClass (45919952-29f4-476d-b0cc-89f0ce5e7f49)
 Call ID: 45919952-29f4-476d-b0cc-89f0ce5e7f49
  Args:
    source: Marie_of_Mecklenburg-Schwerin
    type: :Person
  AddTriple (3e6d869d-1dc3-4d21-bbea-8b2ed8b51d8e)
 Call ID: 3e6d869d-1dc3-4d21-bbea-8b2ed8b51d8e
  Args:
    source: Marie_of_Mecklenburg-Schwerin
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :isMotherOf
  AssignClass (c3068883-6a81-45ce-b15a-27144ed274ef)
 Call ID: c3068883-6a81-45ce-b15a-27144ed274ef
  Args:
    source: Grand_Duke_Kirill_Vladimirovich
    type: :Man
  AssignClass (f58dcd2b-c8a9-4f05-929b-2ffed39c00cc)
 Call ID: f58dcd2b-c8a9-4f05-929b-2ffed39c00cc
  Args:
    type: :Person
    source: Grand_Duke_Kirill_Vladimirovich
  AddTriple (0c326eb5-d20e-4057-bebc-1eea7d863afe)
 Call ID: 0c326eb5-d20e-4057-bebc-1eea7d863afe
  Args:
    target: Grand_Duke_Kirill_Vladimirovich
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :isSiblingOf
  AssignClass (574878b0-bfdd-446c-8299-893a62b03335)
 Call ID: 574878b0-bfdd-446c-8299-893a62b03335
  Args:
    source: Constantine
    type: :Man
  AssignClass (d5b5f309-ebbf-42a6-a867-e3b96a5ca856)
 Call ID: d5b5f309-ebbf-42a6-a867-e3b96a5ca856
  Args:
    source: Constantine
    type: :Person
  AddTriple (266a93d3-9e93-4112-919d-c5998e2ccad3)
 Call ID: 266a93d3-9e93-4112-919d-c5998e2ccad3
  Args:
    target: Constantine
    source: Prince_Nicholas_of_Greece_and_Denmark
    relation: :isSiblingOf
  AssignClass (42423acd-cf9c-432b-85fb-c3cd4fd8aaa8)
 Call ID: 42423acd-cf9c-432b-85fb-c3cd4fd8aaa8
  Args:
    type: :Man
    source: George
  AssignClass (3cbeb618-2c64-44e9-a44e-64d43aa16720)
 Call ID: 3cbeb618-2c64-44e9-a44e-64d43aa16720
  Args:
    type: :Person
    source: George
  AddTriple (002cf022-9381-499f-a627-fc3cf5d8a8a1)
 Call ID: 002cf022-9381-499f-a627-fc3cf5d8a8a1
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    target: George
    relation: :isSiblingOf
  AssignClass (c54581e5-52bd-4d85-b021-922ae212bbe6)
 Call ID: c54581e5-52bd-4d85-b021-922ae212bbe6
  Args:
    type: :Man
    source: George_Simitis
  AssignClass (22dbddca-c793-48b4-a514-536f2f49f420)
 Call ID: 22dbddca-c793-48b4-a514-536f2f49f420
  Args:
    source: George_Simitis
    type: :Person
  AssignClass (b93e6568-a00c-4aef-b069-cf12140200bc)
 Call ID: b93e6568-a00c-4aef-b069-cf12140200bc
  Args:
    type: :Man
    source: Kostas_Simitis
  AssignClass (d5125659-d403-4779-9f36-9caf712089be)
 Call ID: d5125659-d403-4779-9f36-9caf712089be
  Args:
    type: :Person
    source: Kostas_Simitis
  AddTriple (1a620e8f-1709-4fda-88b1-ba99c5a6064e)
 Call ID: 1a620e8f-1709-4fda-88b1-ba99c5a6064e
  Args:
    target: Kostas_Simitis
    source: George_Simitis
    relation: :isFatherOf
  Finish (6b1652ef-df48-4c4d-ab5d-4f59b18e3018)
 Call ID: 6b1652ef-df48-4c4d-ab5d-4f59b18e3018
  Args: