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
Prince Amedeo of Savoy-Aosta, 5th Duke of Aosta (Amedeo Umberto Costantino Giorgio
Early life

Amedeo was born at Villa della Cisterna in Florence, the only child of Prince Aimone, Duke of Aosta, formerly designated king of Croatia as Tomislav II, and of Princess Irene of Greece and Denmark through whom he was a great-great-grandson of Queen Victoria.
When Amedeo was only four years old, his father died in exile in Buenos Aires, and he succeeded him as Duke of Aosta, Prince della Cisterna e Belriguardo, Marchese di Voghera, and Count di Ponderano.
He was an Honorary Companion of the Pennsylvania Commandery of the Military Order of the Loyal Legion of the United States, assigned insignia number 21015, as a great-grandson of Prince Philippe, Count of Paris.
Marriages and family

1st marriage and descendants

On 22 July 1964, at the Igreja Paroquial De São Pedro in Sintra, Portugal, Amedeo married his second cousin, Princess Claude of Orléans (born 11 December 1943).
She was the ninth child and fifth daughter of Henri, comte de Paris, Orléanist claimant to the French throne, and of Princess Isabelle of Orléans-Braganza.
He was involved in various agricultural activities, including the production of wine marketed under the name Vini Savoia Aosta.
Dynastic activities

Amedeo was long viewed by Italian royalists as a likely claimant to the throne if Umberto's own son, Vittorio Emanuele, Prince of Naples, failed to live up to monarchist expectations.
On 7 July 2006, Amedeo declared himself to be the Head of the House of Savoy and Duke of Savoy, claiming that in 1971, Vittorio Emanuele had lost his dynastic rights when he married without previously obtaining the permission of Umberto II, authorization which had been required under monarchical law.
In 2009, Vittorio Emanuele and his son, Emanuele Filiberto, Prince of Venice, sought judicial intervention to forbid Amedeo's use of the surname di Savoia.
In February 2010, the court of Arezzo ruled that the Amedeo and his son Aimone must pay damages totalling 50,000 euros to their cousins and cease using the surname di Savoia instead of di Savoia-Aosta.
Amedeo's claim received the support of Vittorio Emanuele's sister, Princess Maria Gabriella of Savoy.
Although many monarchists transferred their allegiance to Amedeo at some point after King Umberto's death, Amedeo was criticised by other Italian royalists who continue to support Prince Vittorio Emanuele.
But others, including constitutional jurist Guido Locatello, declared the marriage of Vittorio Emanuele to be in violation of Savoy dynastic law years before the scandal evoked any clamour for Amedeo to replace him.
The Unione Monarchica Italiana published in its newsletter, Monarchia Nuova, on 12 February 1987 that the Prince of Naples' marriage to Marina Doria violated the decree of Victor Amadeus III, issued 13 September 1780, regulating the marriages of princes of the blood royal, compelling the Unione to recognise Amedeo as rightful head of the royal house—although at that time Aosta had put forth no public dynastic claim.
Amedeo was a Knight of the Supreme Order of the Most Holy Annunciation named by Umberto II, a Grand Cross of the Order of Saints Maurice and Lazarus named by his cousin Vittorio Emanuele, and a Knight of Honor and Devotion of the Sovereign Military Order of St. John of Jerusalem.
Death

Prince Amedeo died on 1 June 2021, at the age of 77, in Arezzo, Italy, from cardiac arrest after undergoing surgery on 27 May.



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
  AssignClass (4fd13afe-8f49-45d5-83bd-90852956e7b3)
 Call ID: 4fd13afe-8f49-45d5-83bd-90852956e7b3
  Args:
    type: :Man
    source: Amedeo_of_Savoy-Aosta
  AssignClass (2223bbc6-94cc-441d-b7a9-607e532f9d82)
 Call ID: 2223bbc6-94cc-441d-b7a9-607e532f9d82
  Args:
    type: :Person
    source: Amedeo_of_Savoy-Aosta
  AssignClass (1885e119-97d1-43f1-add1-c26b04ae0224)
 Call ID: 1885e119-97d1-43f1-add1-c26b04ae0224
  Args:
    type: :Man
    source: Aimone_Duke_of_Aosta
  AssignClass (3ed14efc-99e7-4561-839e-a687eead8744)
 Call ID: 3ed14efc-99e7-4561-839e-a687eead8744
  Args:
    source: Aimone_Duke_of_Aosta
    type: :Person
  AssignClass (dfff712b-d790-47df-a9f9-135c2e0f4c15)
 Call ID: dfff712b-d790-47df-a9f9-135c2e0f4c15
  Args:
    source: Irene_of_Greece_and_Denmark
    type: :Woman
  AssignClass (ce537f5f-949b-4379-88c7-ea711da0bdc6)
 Call ID: ce537f5f-949b-4379-88c7-ea711da0bdc6
  Args:
    source: Irene_of_Greece_and_Denmark
    type: :Person
  AssignClass (9f84c012-3513-4364-8a6e-30fe64bac3db)
 Call ID: 9f84c012-3513-4364-8a6e-30fe64bac3db
  Args:
    type: :Woman
    source: Claude_of_Orleans
  AssignClass (f7e11b22-cbee-443d-b886-547026798a05)
 Call ID: f7e11b22-cbee-443d-b886-547026798a05
  Args:
    source: Claude_of_Orleans
    type: :Person
  AssignClass (050152b9-e98b-46fb-b205-c5a196539048)
 Call ID: 050152b9-e98b-46fb-b205-c5a196539048
  Args:
    type: :Man
    source: Henri_comte_de_Paris
  AssignClass (ef8c8c76-4acf-493b-af28-da15617047f5)
 Call ID: ef8c8c76-4acf-493b-af28-da15617047f5
  Args:
    source: Henri_comte_de_Paris
    type: :Person
  AssignClass (44afb30f-896c-4c2d-a6f9-44eecb18f9aa)
 Call ID: 44afb30f-896c-4c2d-a6f9-44eecb18f9aa
  Args:
    type: :Woman
    source: Isabelle_of_Orleans-Braganza
  AssignClass (97e7ec0e-cd9f-4c82-8295-87d0c8937e70)
 Call ID: 97e7ec0e-cd9f-4c82-8295-87d0c8937e70
  Args:
    type: :Person
    source: Isabelle_of_Orleans-Braganza
  AssignClass (d4ae696c-8102-4d93-8c8f-b4839ec265a3)
 Call ID: d4ae696c-8102-4d93-8c8f-b4839ec265a3
  Args:
    source: Aimone_son_of_Amedeo
    type: :Man
  AssignClass (e366c9f5-925f-4a85-bf58-9556fc799fde)
 Call ID: e366c9f5-925f-4a85-bf58-9556fc799fde
  Args:
    source: Aimone_son_of_Amedeo
    type: :Person
  AddTriple (3cce76c7-e4ec-4d64-b066-400a3dc59641)
 Call ID: 3cce76c7-e4ec-4d64-b066-400a3dc59641
  Args:
    source: Amedeo_of_Savoy-Aosta
    relation: :hasFather
    target: Aimone_Duke_of_Aosta
  AddTriple (9e2dfa18-b88c-4879-892b-410ef221b575)
 Call ID: 9e2dfa18-b88c-4879-892b-410ef221b575
  Args:
    target: Irene_of_Greece_and_Denmark
    relation: :hasMother
    source: Amedeo_of_Savoy-Aosta
  AddTriple (2c2a7910-56d9-46ca-9056-4cdc1de7393c)
 Call ID: 2c2a7910-56d9-46ca-9056-4cdc1de7393c
  Args:
    target: Henri_comte_de_Paris
    relation: :hasFather
    source: Claude_of_Orleans
  AddTriple (13062c03-c8a3-4ce8-b853-44b45ca6148f)
 Call ID: 13062c03-c8a3-4ce8-b853-44b45ca6148f
  Args:
    source: Claude_of_Orleans
    target: Isabelle_of_Orleans-Braganza
    relation: :hasMother
  AddTriple (e63893d0-c187-41e8-b5ec-4503f6271feb)
 Call ID: e63893d0-c187-41e8-b5ec-4503f6271feb
  Args:
    source: Aimone_son_of_Amedeo
    relation: :hasFather
    target: Amedeo_of_Savoy-Aosta
  AddLiteral (bb9ac964-5c32-4881-b1e7-f236ddee1933)
 Call ID: bb9ac964-5c32-4881-b1e7-f236ddee1933
  Args:
    source: Amedeo_of_Savoy-Aosta
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2021
  AddLiteral (52816520-3c8a-4e20-8db1-a37b384590b5)
 Call ID: 52816520-3c8a-4e20-8db1-a37b384590b5
  Args:
    literal_value: 1943
    literal_type: xsd:integer
    source: Claude_of_Orleans
    relation: :hasBirthYear
  AddLiteral (622c6ff5-b19d-4ec1-a9a7-f545a92e23d7)
 Call ID: 622c6ff5-b19d-4ec1-a9a7-f545a92e23d7
  Args:
    relation: :hasMarriageYear
    source: Amedeo_of_Savoy-Aosta
    literal_type: xsd:integer
    literal_value: 1964
  Finish (10ecf77d-43b7-45df-b276-0a7c21d9b9c6)
 Call ID: 10ecf77d-43b7-45df-b276-0a7c21d9b9c6
  Args: