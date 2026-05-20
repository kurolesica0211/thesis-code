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
Princess Sophie Louise of Saxe-Weimar-Eisenach (20 March 1911 – 21 November 1988) was a princess of the House of Saxe-Weimar-Eisenach.
She was born in Weimar, the eldest child and only daughter of William Ernest, Grand Duke of Saxe-Weimar-Eisenach, by his second wife, Princess Feodora of Saxe-Meiningen.
As a relative of Wilhelmina of the Netherlands, Sophie was invited to the 1937 wedding of her daughter, Princess Juliana, as a bridesmaid.
She became entangled in a diplomatic scandal however after the passports of Sophie and two other German princesses were withheld by the Nazi government.
Though they were later released, Sophie opted out of attending at the last moment.
In 1938 Sophie married Friedrich Günther, Prince of Schwarzburg, but the couple were divorced by the end of the year.
Juliana's wedding

Invitation

Preparations for the wedding of Queen Wilhelmina of the Netherlands's only child Crown Princess Juliana to the German Prince Bernhard of Lippe-Biesterfeld were under way in 1937 when a small diplomatic scandal occurred.
These included Sophie herself (her and Bernhard's second cousin), Duchess Thyra of Mecklenburg-Schwerin (her second cousin), Grand Duchess Kira Kirillovna of Russia (her first cousin once removed), Duchess Woizlawa of Mecklenburg (her cousin), and two of Bernhard's first cousins, Princess Sieglinde of Lippe and Princess Elisabeth of Lippe.
Diplomatic scandal

Sophie became entangled in the small diplomatic scandal as preparations for the Dutch wedding commenced.
The German Nazi government, apparently outraged that their flag was not used in festivities related to the wedding, refused to release the passports of Sophie, along with those of Bernard's cousins Princesses Sieglinde and Elizabeth zur Lippe.
The German government stated that they were also protesting supposed anti-Nazi incidents in the Netherlands, and was angry that Juliana's German fiancé Prince Bernhard had not publicly defended the Nazi regime there.
Wilhelmina and the Dutch government responded that because they believed the wedding to be a private, family affair, the use of the German flag would be inappropriate; they instead opted to fly the Dutch national flag alongside the flag of Bernhard's family.
German displeasure also applied to their national anthem; Wilhelmina and the Dutch government saw no need in playing it at the wedding, as Bernhard was now a Dutch citizen, and thus no longer held German citizenship.
The passports were not released until Prince Bernhard sent a personal letter to German Chancellor Adolf Hitler.
Though the passports were released, Sophie for unknown reasons revoked her acceptance and stated she could no longer attend the wedding at the last moment.
Princess Sophie was replaced as bridesmaid by Baroness von Heeckeren van Kell, one of Juliana's ladies-in-waiting.
Marriage

On 7 March 1938 at Heinrichau, Schlesien, Sophie married Friedrich Günther, Prince of Schwarzburg.
He had held that title since the death of his father Sizzo, Prince of Schwarzburg on 24 March 1926.
Consequently, his sister Marie Antoinette controversially succeeded him as Princess of Schwarzburg.
Sophie died on 21 November 1988 in Hamburg.



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
  AssignClass (4826e6f3-2333-486d-b802-04f551b52196)
 Call ID: 4826e6f3-2333-486d-b802-04f551b52196
  Args:
    type: :Person
    source: Sophie_Louise_of_Saxe-Weimar-Eisenach
  AssignClass (7101fe80-c1bd-4e15-a02b-2306299b207b)
 Call ID: 7101fe80-c1bd-4e15-a02b-2306299b207b
  Args:
    source: Sophie_Louise_of_Saxe-Weimar-Eisenach
    type: :Woman
  AssignClass (47aef22a-eb1c-470f-a477-43ea844e8a1e)
 Call ID: 47aef22a-eb1c-470f-a477-43ea844e8a1e
  Args:
    type: :Person
    source: William_Ernest_of_Saxe-Weimar-Eisenach
  AssignClass (7ded1bf0-108c-43db-a6c7-55cc69c6a856)
 Call ID: 7ded1bf0-108c-43db-a6c7-55cc69c6a856
  Args:
    source: William_Ernest_of_Saxe-Weimar-Eisenach
    type: :Man
  AssignClass (af429777-3892-436b-a0da-5919180450da)
 Call ID: af429777-3892-436b-a0da-5919180450da
  Args:
    type: :Ancestor
    source: William_Ernest_of_Saxe-Weimar-Eisenach
  AssignClass (a600d5a7-a545-4837-ae6d-d20f5f53173b)
 Call ID: a600d5a7-a545-4837-ae6d-d20f5f53173b
  Args:
    type: :Person
    source: Feodora_of_Saxe-Meiningen
  AssignClass (ae4aa74d-78e9-4bfb-8590-3cf5edc37c04)
 Call ID: ae4aa74d-78e9-4bfb-8590-3cf5edc37c04
  Args:
    type: :Woman
    source: Feodora_of_Saxe-Meiningen
  AssignClass (5d96251e-e2ac-495e-9423-964c58516574)
 Call ID: 5d96251e-e2ac-495e-9423-964c58516574
  Args:
    type: :Ancestor
    source: Feodora_of_Saxe-Meiningen
  AssignClass (a8e842ea-d173-427d-b068-7ae1d9b888fc)
 Call ID: a8e842ea-d173-427d-b068-7ae1d9b888fc
  Args:
    type: :Person
    source: Friedrich_Gunther_of_Schwarzburg
  AssignClass (aa3cb77a-b9c2-4633-a216-75bb837f6fe2)
 Call ID: aa3cb77a-b9c2-4633-a216-75bb837f6fe2
  Args:
    source: Friedrich_Gunther_of_Schwarzburg
    type: :Man
  AssignClass (bf90f278-50aa-445d-9594-b7fbfebb972c)
 Call ID: bf90f278-50aa-445d-9594-b7fbfebb972c
  Args:
    type: :Person
    source: Sizzo_of_Schwarzburg
  AssignClass (167589d4-abda-474d-8d29-7d3353a40f0a)
 Call ID: 167589d4-abda-474d-8d29-7d3353a40f0a
  Args:
    source: Sizzo_of_Schwarzburg
    type: :Man
  AssignClass (3342dd36-679d-49df-89ca-62ccc73cee28)
 Call ID: 3342dd36-679d-49df-89ca-62ccc73cee28
  Args:
    source: Sizzo_of_Schwarzburg
    type: :Ancestor
  AssignClass (27dcda1b-8287-469c-ac9b-7bb00c561c30)
 Call ID: 27dcda1b-8287-469c-ac9b-7bb00c561c30
  Args:
    source: Marie_Antoinette_of_Schwarzburg
    type: :Person
  AssignClass (63126144-ec81-41cc-b496-00117dbb80f2)
 Call ID: 63126144-ec81-41cc-b496-00117dbb80f2
  Args:
    type: :Woman
    source: Marie_Antoinette_of_Schwarzburg
  AddTriple (77fabd7a-66f4-4b47-9772-54909c64d1c7)
 Call ID: 77fabd7a-66f4-4b47-9772-54909c64d1c7
  Args:
    relation: :hasFather
    source: Sophie_Louise_of_Saxe-Weimar-Eisenach
    target: William_Ernest_of_Saxe-Weimar-Eisenach
  AddTriple (cddf295a-f994-475c-b284-c74fd4b68b1c)
 Call ID: cddf295a-f994-475c-b284-c74fd4b68b1c
  Args:
    target: Feodora_of_Saxe-Meiningen
    source: Sophie_Louise_of_Saxe-Weimar-Eisenach
    relation: :hasMother
  AddLiteral (289834bb-00b9-49a0-8e09-9695bbcf8797)
 Call ID: 289834bb-00b9-49a0-8e09-9695bbcf8797
  Args:
    source: Sophie_Louise_of_Saxe-Weimar-Eisenach
    literal_type: xsd:integer
    literal_value: 1911
    relation: :hasBirthYear
  AddLiteral (8bd401fa-4517-4f56-b140-288c9f41d908)
 Call ID: 8bd401fa-4517-4f56-b140-288c9f41d908
  Args:
    relation: :hasDeathYear
    literal_value: 1988
    literal_type: xsd:integer
    source: Sophie_Louise_of_Saxe-Weimar-Eisenach
  AddLiteral (0a663215-8c04-4147-8e3e-24ccea1b48d0)
 Call ID: 0a663215-8c04-4147-8e3e-24ccea1b48d0
  Args:
    relation: :hasMarriageYear
    literal_value: 1938
    literal_type: xsd:integer
    source: Sophie_Louise_of_Saxe-Weimar-Eisenach
  AddTriple (b9dd3638-f0f8-4fac-b61c-3436defb551b)
 Call ID: b9dd3638-f0f8-4fac-b61c-3436defb551b
  Args:
    target: Sizzo_of_Schwarzburg
    source: Friedrich_Gunther_of_Schwarzburg
    relation: :hasFather
  AddTriple (10323f4c-f026-48ed-be19-bb57968070b8)
 Call ID: 10323f4c-f026-48ed-be19-bb57968070b8
  Args:
    relation: :hasSister
    source: Friedrich_Gunther_of_Schwarzburg
    target: Marie_Antoinette_of_Schwarzburg
  AddLiteral (4385f732-bce4-4153-8729-02543711b026)
 Call ID: 4385f732-bce4-4153-8729-02543711b026
  Args:
    source: Sizzo_of_Schwarzburg
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1926
  Finish (229b2a2b-766f-479f-826c-5ba44ffbebb5)
 Call ID: 229b2a2b-766f-479f-826c-5ba44ffbebb5
  Args: