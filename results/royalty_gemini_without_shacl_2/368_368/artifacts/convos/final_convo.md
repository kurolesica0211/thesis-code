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
Leopold IV, Prince of Lippe (Leopold Julius Bernhard Adalbert Otto Karl Gustav; 30 May 1871 – 30 December 1949) was the final sovereign of the Principality of Lippe in northwestern Germany from 1905 until his abdication in 1918.
He was the first and only ruler of Lippe of the Lippe-Biesterfeld branch.
Early life

He was born as Count Leopold of Lippe-Biesterfeld in Oberkassel, the son of Ernest, Count of Lippe-Biesterfeld and Countess Karoline of Wartensleben.
Leopold belonged to the Lippe-Biesterfeld line of the House of Lippe which was the most senior line of the princely house after the reigning Lippe-Detmold line.
Ruler of Lippe

Since 1895, the Principality of Lippe had been ruled by a regent due to the incapacity of Prince Alexander.
Leopold's father had acted as regent since 1897, and following his death on 26 September 1904, Leopold assumed the regency.
This was not recognized by the German Emperor Wilhelm II, who initially refused to legally recognize Leopold as regent as there was an issue over whether Leopold and his siblings were of legitimate rank, and as such eligible for the succession.
As a result, the Diet of Lippe appointed a high commission to consider the matter.
The regency issue was still ongoing when Prince Alexander died on 13 January 1905.
Leopold was confirmed as Prince of Lippe and Alexander's successor on 25 October 1905, following a court ruling.
On 3 June 1911, while out motoring, Leopold and his brother Prince Julius were attacked by a gang of Italian laborers who hurled a shower of missiles at the princes.
Though Leopold escaped unhurt, his brother received a head wound.
During World War I, Leopold upgraded the titles of the various lines of the House of Lippe.
One of the members to benefit from the granting of titles was Leopold's nephew Count Bernhard of Biesterfeld (son of Leopold's brother Bernhard), who would go on to become the Prince Consort of Queen Juliana of the Netherlands.
On 24 February 1916, Bernhard and his brother were upgraded to the title Prince of Lippe-Biesterfeld with the style Serene Highness.
The Counts of Lippe-Weissenfeld also benefited with creations of the title Prince of Lippe-Weissenfeld, with the style Serene Highness, taking place on 24 February 1916 for Count Clemens and his descendants, and again on 9 November 1918 for the other members of this line.
Just three days after upgrading the titles of members of the Lippe-Weissenfeld line, and following the German Empire's defeat in World War I and the subsequent revolution, Leopold was forced to renounce the throne on 12 November 1918.
Following the end of his rule, the Principality of Lippe was transformed into a Free state in the new Weimar Republic.
His eldest son the Hereditary Prince Ernst is reported to have been the first German prince to join the party when he signed up in May 1928.
In addition to being pro Nazi, both Hereditary Prince Ernst and Prince Chlodwig had contracted unequal marriages.
So in 1947 when Leopold wrote his will, Armin, his youngest son and only child with his second wife, would succeed him as head of the House of Lippe and also become administrator of the princely family's properties such as Schloss Detmold.
Thus when Leopold died in Detmold his three eldest sons were all disinherited and his youngest son Armin became head of the princely house.
Marriages and children

Leopold was married to Princess Bertha of Hesse-Philippsthal-Barchfeld (1874–1919) on 16 August 1901 in Rotenburg.



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
  AssignClass (cc98d66d-5308-475f-bf9c-39e4d98cab79)
 Call ID: cc98d66d-5308-475f-bf9c-39e4d98cab79
  Args:
    type: :Man
    source: Leopold_IV_Prince_of_Lippe
  AssignClass (11548c85-74b5-4e2e-a896-18863be01bb4)
 Call ID: 11548c85-74b5-4e2e-a896-18863be01bb4
  Args:
    type: :Person
    source: Leopold_IV_Prince_of_Lippe
  AddLiteral (a432bf17-c077-4591-947c-a3d31e1e2920)
 Call ID: a432bf17-c077-4591-947c-a3d31e1e2920
  Args:
    literal_type: xsd:integer
    source: Leopold_IV_Prince_of_Lippe
    literal_value: 1871
    relation: :hasBirthYear
  AddLiteral (272f0170-3b4b-4ba9-a880-789411777507)
 Call ID: 272f0170-3b4b-4ba9-a880-789411777507
  Args:
    literal_type: xsd:integer
    source: Leopold_IV_Prince_of_Lippe
    relation: :hasDeathYear
    literal_value: 1949
  AssignClass (86566c9b-c931-4762-9ebf-d66d7d148a88)
 Call ID: 86566c9b-c931-4762-9ebf-d66d7d148a88
  Args:
    type: :Man
    source: Ernest_Count_of_Lippe-Biesterfeld
  AssignClass (9babf854-86d4-4ca8-b654-90e9210f1ad8)
 Call ID: 9babf854-86d4-4ca8-b654-90e9210f1ad8
  Args:
    type: :Person
    source: Ernest_Count_of_Lippe-Biesterfeld
  AssignClass (23069ab7-6b2b-44fe-9b95-3d8e30252c2f)
 Call ID: 23069ab7-6b2b-44fe-9b95-3d8e30252c2f
  Args:
    type: :Woman
    source: Karoline_of_Wartensleben
  AssignClass (ed175f9f-e473-4216-a234-f5d3bd347fcc)
 Call ID: ed175f9f-e473-4216-a234-f5d3bd347fcc
  Args:
    type: :Person
    source: Karoline_of_Wartensleben
  AddTriple (21991805-c623-4014-ac57-98d012e00f58)
 Call ID: 21991805-c623-4014-ac57-98d012e00f58
  Args:
    relation: :hasFather
    target: Ernest_Count_of_Lippe-Biesterfeld
    source: Leopold_IV_Prince_of_Lippe
  AddTriple (35efd1c3-5de0-4119-90d6-0279bf26c6b6)
 Call ID: 35efd1c3-5de0-4119-90d6-0279bf26c6b6
  Args:
    source: Leopold_IV_Prince_of_Lippe
    target: Karoline_of_Wartensleben
    relation: :hasMother
  AssignClass (f727524e-7931-4ff1-b47c-b2caecd56d3f)
 Call ID: f727524e-7931-4ff1-b47c-b2caecd56d3f
  Args:
    type: :Man
    source: Prince_Julius
  AssignClass (a6cf6a42-2aef-45de-b938-d23a3d82e58c)
 Call ID: a6cf6a42-2aef-45de-b938-d23a3d82e58c
  Args:
    type: :Person
    source: Prince_Julius
  AddTriple (059cc0c2-3c33-4e93-a7f2-e0d0e4a84d29)
 Call ID: 059cc0c2-3c33-4e93-a7f2-e0d0e4a84d29
  Args:
    target: Prince_Julius
    relation: :isSiblingOf
    source: Leopold_IV_Prince_of_Lippe
  AssignClass (6949de11-5895-417c-b50b-4f06d27a1d8b)
 Call ID: 6949de11-5895-417c-b50b-4f06d27a1d8b
  Args:
    type: :Man
    source: Bernhard_of_Biesterfeld_nephew
  AssignClass (3e1d624a-8e89-4b6a-ae49-49381e29cfe8)
 Call ID: 3e1d624a-8e89-4b6a-ae49-49381e29cfe8
  Args:
    type: :Person
    source: Bernhard_of_Biesterfeld_nephew
  AssignClass (f1978032-c029-4412-b3ce-0f30b3513e3e)
 Call ID: f1978032-c029-4412-b3ce-0f30b3513e3e
  Args:
    type: :Man
    source: Bernhard_of_Biesterfeld_father
  AssignClass (d5dd126e-6508-414d-8c8e-08063ac63612)
 Call ID: d5dd126e-6508-414d-8c8e-08063ac63612
  Args:
    type: :Person
    source: Bernhard_of_Biesterfeld_father
  AddTriple (86b0d6cd-4969-4dbc-b83e-d6dc42367a5a)
 Call ID: 86b0d6cd-4969-4dbc-b83e-d6dc42367a5a
  Args:
    source: Leopold_IV_Prince_of_Lippe
    relation: :isSiblingOf
    target: Bernhard_of_Biesterfeld_father
  AddTriple (bb524fd9-ed2c-4733-9559-72ae3e93ea04)
 Call ID: bb524fd9-ed2c-4733-9559-72ae3e93ea04
  Args:
    source: Bernhard_of_Biesterfeld_father
    target: Bernhard_of_Biesterfeld_nephew
    relation: :hasSon
  AssignClass (e61762c1-a0b5-4b70-8086-d78396ddac3e)
 Call ID: e61762c1-a0b5-4b70-8086-d78396ddac3e
  Args:
    type: :Man
    source: Ernst_Hereditary_Prince
  AssignClass (ec9bba18-d9d4-4f7e-85a9-ba993edba635)
 Call ID: ec9bba18-d9d4-4f7e-85a9-ba993edba635
  Args:
    type: :Person
    source: Ernst_Hereditary_Prince
  AddTriple (3e791b92-d079-4cb8-b2fc-a6412ec6b9b1)
 Call ID: 3e791b92-d079-4cb8-b2fc-a6412ec6b9b1
  Args:
    relation: :hasSon
    target: Ernst_Hereditary_Prince
    source: Leopold_IV_Prince_of_Lippe
  AssignClass (34bafdb3-ec68-414b-b42a-0c8e427aed63)
 Call ID: 34bafdb3-ec68-414b-b42a-0c8e427aed63
  Args:
    type: :Man
    source: Chlodwig
  AssignClass (b5190358-5043-492c-8863-acd7967f5ecf)
 Call ID: b5190358-5043-492c-8863-acd7967f5ecf
  Args:
    type: :Person
    source: Chlodwig
  AddTriple (af654db6-5809-4446-b2a0-777cc679b534)
 Call ID: af654db6-5809-4446-b2a0-777cc679b534
  Args:
    source: Leopold_IV_Prince_of_Lippe
    target: Chlodwig
    relation: :hasSon
  AssignClass (d04cd446-f55c-4939-a98e-73a458b5c7b5)
 Call ID: d04cd446-f55c-4939-a98e-73a458b5c7b5
  Args:
    type: :Man
    source: Armin
  AssignClass (91ba97e7-9f93-4621-b458-c14dd1ac218f)
 Call ID: 91ba97e7-9f93-4621-b458-c14dd1ac218f
  Args:
    type: :Person
    source: Armin
  AddTriple (1c8cb16d-03e9-436a-baa7-f08532f8c48d)
 Call ID: 1c8cb16d-03e9-436a-baa7-f08532f8c48d
  Args:
    target: Armin
    relation: :hasSon
    source: Leopold_IV_Prince_of_Lippe
  AssignClass (26e6b5ad-0686-46f1-8cdb-32e48f161fb5)
 Call ID: 26e6b5ad-0686-46f1-8cdb-32e48f161fb5
  Args:
    type: :Woman
    source: Princess_Bertha_of_Hesse-Philippsthal-Barchfeld
  AssignClass (e5879f04-eee2-4e39-b73d-83d296b0c6f1)
 Call ID: e5879f04-eee2-4e39-b73d-83d296b0c6f1
  Args:
    type: :Person
    source: Princess_Bertha_of_Hesse-Philippsthal-Barchfeld
  AddLiteral (49158e0a-1517-423f-a99b-57a16aa2ef97)
 Call ID: 49158e0a-1517-423f-a99b-57a16aa2ef97
  Args:
    source: Leopold_IV_Prince_of_Lippe
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1901
  AddLiteral (6942c9e4-4183-4f42-9e93-33a81a4c889f)
 Call ID: 6942c9e4-4183-4f42-9e93-33a81a4c889f
  Args:
    source: Princess_Bertha_of_Hesse-Philippsthal-Barchfeld
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1874
  AddLiteral (60db738d-5f86-4024-a628-83d31402b414)
 Call ID: 60db738d-5f86-4024-a628-83d31402b414
  Args:
    source: Princess_Bertha_of_Hesse-Philippsthal-Barchfeld
    literal_type: xsd:integer
    literal_value: 1919
    relation: :hasDeathYear
  Finish (d346d314-fa48-4ea4-924a-da08a27cd7f0)
 Call ID: d346d314-fa48-4ea4-924a-da08a27cd7f0
  Args: