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
  AssignClass (30aeec92-f61f-4c41-b5e8-e97a30802b50)
 Call ID: 30aeec92-f61f-4c41-b5e8-e97a30802b50
  Args:
    type: :Person
    source: :Sophie_Louise_of_Saxe-Weimar-Eisenach
  AssignClass (a59b85ed-6bc8-4820-9185-ca69d641f29a)
 Call ID: a59b85ed-6bc8-4820-9185-ca69d641f29a
  Args:
    type: :Woman
    source: :Sophie_Louise_of_Saxe-Weimar-Eisenach
  AddLiteral (eb79e7ed-0823-44fd-bfe9-4aebd66a9eed)
 Call ID: eb79e7ed-0823-44fd-bfe9-4aebd66a9eed
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Sophie_Louise_of_Saxe-Weimar-Eisenach
    literal_value: 1911
  AddLiteral (2910535b-fec4-4c75-9029-64bac77305b6)
 Call ID: 2910535b-fec4-4c75-9029-64bac77305b6
  Args:
    source: :Sophie_Louise_of_Saxe-Weimar-Eisenach
    literal_value: 1988
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (e4eaa67b-a6c4-4eba-9b10-2792c3f75e3b)
 Call ID: e4eaa67b-a6c4-4eba-9b10-2792c3f75e3b
  Args:
    type: :Person
    source: :William_Ernest_Grand_Duke_of_Saxe-Weimar-Eisenach
  AssignClass (7bc8604c-25a2-4c69-a46e-f683b7c74bac)
 Call ID: 7bc8604c-25a2-4c69-a46e-f683b7c74bac
  Args:
    type: :Man
    source: :William_Ernest_Grand_Duke_of_Saxe-Weimar-Eisenach
  AssignClass (cc5c8f15-e63f-458c-a586-9b55d257e73b)
 Call ID: cc5c8f15-e63f-458c-a586-9b55d257e73b
  Args:
    type: :Person
    source: :Feodora_of_Saxe-Meiningen
  AssignClass (594c7a8b-8402-4f91-a1cc-6d51a6feb4b7)
 Call ID: 594c7a8b-8402-4f91-a1cc-6d51a6feb4b7
  Args:
    type: :Woman
    source: :Feodora_of_Saxe-Meiningen
  AddTriple (f44b9628-9d4f-49d5-93e7-29fbd6d6ab45)
 Call ID: f44b9628-9d4f-49d5-93e7-29fbd6d6ab45
  Args:
    relation: :hasFather
    source: :Sophie_Louise_of_Saxe-Weimar-Eisenach
    target: :William_Ernest_Grand_Duke_of_Saxe-Weimar-Eisenach
  AddTriple (3ee70b14-35dc-4814-96a4-4ea2122c6e17)
 Call ID: 3ee70b14-35dc-4814-96a4-4ea2122c6e17
  Args:
    relation: :hasMother
    target: :Feodora_of_Saxe-Meiningen
    source: :Sophie_Louise_of_Saxe-Weimar-Eisenach
  AssignClass (349f45ab-2e1e-4c8b-81a8-5bbe14c56810)
 Call ID: 349f45ab-2e1e-4c8b-81a8-5bbe14c56810
  Args:
    type: :Person
    source: :Friedrich_Gunther_Prince_of_Schwarzburg
  AssignClass (04ff8e32-cb53-42a3-ad16-c6513483ca24)
 Call ID: 04ff8e32-cb53-42a3-ad16-c6513483ca24
  Args:
    type: :Man
    source: :Friedrich_Gunther_Prince_of_Schwarzburg
  AddLiteral (5bcee95b-f9c5-4e17-8c7c-b2f70305ad17)
 Call ID: 5bcee95b-f9c5-4e17-8c7c-b2f70305ad17
  Args:
    source: :Sophie_Louise_of_Saxe-Weimar-Eisenach
    literal_value: 1938
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (bdbe2004-eef8-41b3-935a-5b5ddd516017)
 Call ID: bdbe2004-eef8-41b3-935a-5b5ddd516017
  Args:
    target: :Friedrich_Gunther_Prince_of_Schwarzburg
    source: :Sophie_Louise_of_Saxe-Weimar-Eisenach
    relation: :hasRelation
  AssignClass (c65783e4-4349-4fb1-bef9-69242d2f8d30)
 Call ID: c65783e4-4349-4fb1-bef9-69242d2f8d30
  Args:
    type: :Person
    source: :Marie_Antoinette_of_Schwarzburg
  AssignClass (13f2bebe-2892-4963-ac0a-af448d8c7154)
 Call ID: 13f2bebe-2892-4963-ac0a-af448d8c7154
  Args:
    type: :Woman
    source: :Marie_Antoinette_of_Schwarzburg
  AddTriple (4f43a83b-d9fb-44c1-a260-aeee9362175d)
 Call ID: 4f43a83b-d9fb-44c1-a260-aeee9362175d
  Args:
    relation: :hasBrother
    source: :Marie_Antoinette_of_Schwarzburg
    target: :Friedrich_Gunther_Prince_of_Schwarzburg
  Finish (75710f3f-b64b-4bb8-a1e3-779bbcdf4560)
 Call ID: 75710f3f-b64b-4bb8-a1e3-779bbcdf4560
  Args: