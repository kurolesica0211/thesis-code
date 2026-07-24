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
Though the passports were released, Sophie for unknown reasons revoked her acceptance and stated she could no longer attend the wedding at the last moment.
Princess Sophie was replaced as bridesmaid by Baroness von Heeckeren van Kell, one of Juliana's ladies-in-waiting.
Marriage

On 7 March 1938 at Heinrichau, Schlesien, Sophie married Friedrich Günther, Prince of Schwarzburg.
Consequently, his sister Marie Antoinette controversially succeeded him as Princess of Schwarzburg.
Sophie died on 21 November 1988 in Hamburg.



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
  AssignClass (ee3912ff-55c0-4c0e-a56b-535aa4dd5f15)
 Call ID: ee3912ff-55c0-4c0e-a56b-535aa4dd5f15
  Args:
    type: :Woman
    source: Sophie_Louise_of_Saxe-Weimar-Eisenach
  AssignClass (94044515-1a10-48aa-a212-746135f0c544)
 Call ID: 94044515-1a10-48aa-a212-746135f0c544
  Args:
    source: Sophie_Louise_of_Saxe-Weimar-Eisenach
    type: :Person
  AddLiteral (4d5c5f4b-6df7-4130-a134-ee12b2f0611d)
 Call ID: 4d5c5f4b-6df7-4130-a134-ee12b2f0611d
  Args:
    relation: :hasBirthYear
    source: Sophie_Louise_of_Saxe-Weimar-Eisenach
    literal_type: xsd:positiveInteger
    literal_value: 1911
  AddLiteral (a36ba3b1-3dbe-4e01-8055-34a9d1a79f9a)
 Call ID: a36ba3b1-3dbe-4e01-8055-34a9d1a79f9a
  Args:
    literal_value: 1988
    source: Sophie_Louise_of_Saxe-Weimar-Eisenach
    relation: :hasDeathYear
    literal_type: xsd:positiveInteger
  AssignClass (e8ca3871-5a55-4ba2-a3b9-06cd9fe4ede4)
 Call ID: e8ca3871-5a55-4ba2-a3b9-06cd9fe4ede4
  Args:
    source: William_Ernest_of_Saxe-Weimar-Eisenach
    type: :Man
  AssignClass (23012a90-c03f-4d27-91b0-5dcd8d07abf2)
 Call ID: 23012a90-c03f-4d27-91b0-5dcd8d07abf2
  Args:
    source: William_Ernest_of_Saxe-Weimar-Eisenach
    type: :Person
  AssignClass (24ce7b02-e288-4167-8158-c00acbe147de)
 Call ID: 24ce7b02-e288-4167-8158-c00acbe147de
  Args:
    source: Feodora_of_Saxe-Meiningen
    type: :Woman
  AssignClass (d5e5e47b-f30f-4715-a9c7-f1c760e1092e)
 Call ID: d5e5e47b-f30f-4715-a9c7-f1c760e1092e
  Args:
    source: Feodora_of_Saxe-Meiningen
    type: :Person
  AddTriple (c3c84038-b67f-4d0a-976f-156b383ec4ac)
 Call ID: c3c84038-b67f-4d0a-976f-156b383ec4ac
  Args:
    target: William_Ernest_of_Saxe-Weimar-Eisenach
    source: Sophie_Louise_of_Saxe-Weimar-Eisenach
    relation: :hasFather
  AddTriple (3a5a4bec-8d82-4045-a458-bc12a7f87697)
 Call ID: 3a5a4bec-8d82-4045-a458-bc12a7f87697
  Args:
    source: Sophie_Louise_of_Saxe-Weimar-Eisenach
    relation: :hasMother
    target: Feodora_of_Saxe-Meiningen
  AssignClass (29ee2f1e-d141-46a9-a0f1-23e866763346)
 Call ID: 29ee2f1e-d141-46a9-a0f1-23e866763346
  Args:
    type: :Man
    source: Friedrich_Gunther_of_Schwarzburg
  AssignClass (1220c062-644b-46b3-8dae-087dd9687224)
 Call ID: 1220c062-644b-46b3-8dae-087dd9687224
  Args:
    type: :Person
    source: Friedrich_Gunther_of_Schwarzburg
  AddLiteral (a007ddaf-791c-4577-a0d5-46e2eb78c227)
 Call ID: a007ddaf-791c-4577-a0d5-46e2eb78c227
  Args:
    literal_type: xsd:positiveInteger
    relation: :hasMarriageYear
    source: Sophie_Louise_of_Saxe-Weimar-Eisenach
    literal_value: 1938
  AddTriple (f5e0c8f3-9b6f-4b07-95bc-0a20efd204e3)
 Call ID: f5e0c8f3-9b6f-4b07-95bc-0a20efd204e3
  Args:
    source: Sophie_Louise_of_Saxe-Weimar-Eisenach
    relation: :hasRelation
    target: Friedrich_Gunther_of_Schwarzburg
  AssignClass (6e6f46c0-fd78-4b66-a041-b9edee4cebad)
 Call ID: 6e6f46c0-fd78-4b66-a041-b9edee4cebad
  Args:
    type: :Woman
    source: Marie_Antoinette_of_Schwarzburg
  AssignClass (40fed58f-eec1-4b69-a9bd-f76763d89de1)
 Call ID: 40fed58f-eec1-4b69-a9bd-f76763d89de1
  Args:
    source: Marie_Antoinette_of_Schwarzburg
    type: :Person
  AddTriple (ed8529d0-7e01-4516-90ca-4b91987460a2)
 Call ID: ed8529d0-7e01-4516-90ca-4b91987460a2
  Args:
    target: Marie_Antoinette_of_Schwarzburg
    source: Friedrich_Gunther_of_Schwarzburg
    relation: :hasSister
  AssignClass (f92bbd04-7887-4631-b1a3-c76922d2b1d4)
 Call ID: f92bbd04-7887-4631-b1a3-c76922d2b1d4
  Args:
    source: Wilhelmina_of_the_Netherlands
    type: :Woman
  AssignClass (6e400202-e3a5-41e5-89f6-76fb6db1dbc1)
 Call ID: 6e400202-e3a5-41e5-89f6-76fb6db1dbc1
  Args:
    source: Wilhelmina_of_the_Netherlands
    type: :Person
  AssignClass (83ce6fcf-7ce6-4806-97d5-2a51f71aab6e)
 Call ID: 83ce6fcf-7ce6-4806-97d5-2a51f71aab6e
  Args:
    source: Juliana_of_the_Netherlands
    type: :Woman
  AssignClass (2b81847b-9a03-434b-8fda-175c32f30930)
 Call ID: 2b81847b-9a03-434b-8fda-175c32f30930
  Args:
    type: :Person
    source: Juliana_of_the_Netherlands
  AddTriple (10f7894e-4175-46e8-b20b-ffc4dad27c2f)
 Call ID: 10f7894e-4175-46e8-b20b-ffc4dad27c2f
  Args:
    target: Wilhelmina_of_the_Netherlands
    relation: :hasMother
    source: Juliana_of_the_Netherlands
  AssignClass (7a1dcaeb-feea-4e98-9908-ee59bb8ff1ac)
 Call ID: 7a1dcaeb-feea-4e98-9908-ee59bb8ff1ac
  Args:
    source: Bernhard_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (c0b07357-40d0-4e9b-9611-c42a16db4c3a)
 Call ID: c0b07357-40d0-4e9b-9611-c42a16db4c3a
  Args:
    source: Bernhard_of_Lippe-Biesterfeld
    type: :Person
  Finish (7c86fe06-785e-4ef8-bdb3-38e2a960bd8e)
 Call ID: 7c86fe06-785e-4ef8-bdb3-38e2a960bd8e
  Args: