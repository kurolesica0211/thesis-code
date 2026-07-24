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
  AssignClass (a498bb90-1e59-48cc-8a41-4130a20fb32c)
 Call ID: a498bb90-1e59-48cc-8a41-4130a20fb32c
  Args:
    type: :Man
    source: :Leopold_IV_Prince_of_Lippe
  AssignClass (48caea7f-e13a-4731-9b1a-be5fb37e1ce2)
 Call ID: 48caea7f-e13a-4731-9b1a-be5fb37e1ce2
  Args:
    source: :Leopold_IV_Prince_of_Lippe
    type: :Person
  AddLiteral (48a07969-d327-429a-96ef-5acba8c67a65)
 Call ID: 48a07969-d327-429a-96ef-5acba8c67a65
  Args:
    literal_value: 1871
    source: :Leopold_IV_Prince_of_Lippe
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (0ec8485c-adab-4ce1-926d-57506d2d7c09)
 Call ID: 0ec8485c-adab-4ce1-926d-57506d2d7c09
  Args:
    literal_value: 1949
    source: :Leopold_IV_Prince_of_Lippe
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (40c27fcb-b6d9-4efe-8123-444d44c2f566)
 Call ID: 40c27fcb-b6d9-4efe-8123-444d44c2f566
  Args:
    type: :Man
    source: :Ernest_Count_of_Lippe-Biesterfeld
  AssignClass (83040347-bc9b-4168-911c-2ec2ba1e91e3)
 Call ID: 83040347-bc9b-4168-911c-2ec2ba1e91e3
  Args:
    source: :Ernest_Count_of_Lippe-Biesterfeld
    type: :Person
  AssignClass (979b09e7-eb9f-4aa2-95cd-0a9391913af2)
 Call ID: 979b09e7-eb9f-4aa2-95cd-0a9391913af2
  Args:
    type: :Woman
    source: :Karoline_of_Wartensleben
  AssignClass (3f78153c-1dfb-4938-a8ad-a18c30a523f7)
 Call ID: 3f78153c-1dfb-4938-a8ad-a18c30a523f7
  Args:
    source: :Karoline_of_Wartensleben
    type: :Person
  AddTriple (15cbbd01-b50e-4b09-a6be-bd580b01071d)
 Call ID: 15cbbd01-b50e-4b09-a6be-bd580b01071d
  Args:
    relation: :hasFather
    target: :Ernest_Count_of_Lippe-Biesterfeld
    source: :Leopold_IV_Prince_of_Lippe
  AddTriple (a6db3ac8-33fd-4378-8834-74f749a2d3f7)
 Call ID: a6db3ac8-33fd-4378-8834-74f749a2d3f7
  Args:
    relation: :hasMother
    source: :Leopold_IV_Prince_of_Lippe
    target: :Karoline_of_Wartensleben
  AssignClass (5a84e5b8-9fa1-4d81-a165-09bd4e89b2ce)
 Call ID: 5a84e5b8-9fa1-4d81-a165-09bd4e89b2ce
  Args:
    source: :Prince_Julius
    type: :Man
  AssignClass (a35d2818-b853-4014-a739-4a06136d06a4)
 Call ID: a35d2818-b853-4014-a739-4a06136d06a4
  Args:
    type: :Person
    source: :Prince_Julius
  AddTriple (9d001f57-f429-4f89-a0a9-eeeebc4ba59c)
 Call ID: 9d001f57-f429-4f89-a0a9-eeeebc4ba59c
  Args:
    relation: :hasBrother
    target: :Prince_Julius
    source: :Leopold_IV_Prince_of_Lippe
  AssignClass (413da9b2-2ef8-4a7d-b826-fbda55a628eb)
 Call ID: 413da9b2-2ef8-4a7d-b826-fbda55a628eb
  Args:
    type: :Woman
    source: :Princess_Bertha_of_Hesse-Philippsthal-Barchfeld
  AssignClass (55254b11-7376-4080-b2a4-b0ba38337803)
 Call ID: 55254b11-7376-4080-b2a4-b0ba38337803
  Args:
    source: :Princess_Bertha_of_Hesse-Philippsthal-Barchfeld
    type: :Person
  AddLiteral (8f104d6b-72d2-4d80-a10e-aa02b452a533)
 Call ID: 8f104d6b-72d2-4d80-a10e-aa02b452a533
  Args:
    literal_value: 1901
    source: :Leopold_IV_Prince_of_Lippe
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (8ad7fa4e-2803-4203-8ba9-980285528b9d)
 Call ID: 8ad7fa4e-2803-4203-8ba9-980285528b9d
  Args:
    relation: :hasRelation
    source: :Leopold_IV_Prince_of_Lippe
    target: :Princess_Bertha_of_Hesse-Philippsthal-Barchfeld
  AssignClass (8a7cb929-da6b-405f-964a-1b3f32a794c6)
 Call ID: 8a7cb929-da6b-405f-964a-1b3f32a794c6
  Args:
    source: :Hereditary_Prince_Ernst
    type: :Man
  AssignClass (55c9cce3-d6c7-4749-bb08-cfd570c56fcf)
 Call ID: 55c9cce3-d6c7-4749-bb08-cfd570c56fcf
  Args:
    source: :Hereditary_Prince_Ernst
    type: :Person
  AddTriple (9cd6aa48-22f1-483b-b7ff-edaf4bf489d8)
 Call ID: 9cd6aa48-22f1-483b-b7ff-edaf4bf489d8
  Args:
    relation: :hasSon
    target: :Hereditary_Prince_Ernst
    source: :Leopold_IV_Prince_of_Lippe
  AssignClass (0a752661-e6d9-4029-b49a-79fc33d68c7f)
 Call ID: 0a752661-e6d9-4029-b49a-79fc33d68c7f
  Args:
    type: :Man
    source: :Prince_Chlodwig
  AssignClass (284e4c3a-dc0f-4326-b477-6af6e960b0f6)
 Call ID: 284e4c3a-dc0f-4326-b477-6af6e960b0f6
  Args:
    type: :Person
    source: :Prince_Chlodwig
  AddTriple (4dc56962-d21f-47ac-a689-e2dce47482c8)
 Call ID: 4dc56962-d21f-47ac-a689-e2dce47482c8
  Args:
    target: :Prince_Chlodwig
    source: :Leopold_IV_Prince_of_Lippe
    relation: :hasSon
  AssignClass (cc097d94-46d6-4164-928b-6426d06e903b)
 Call ID: cc097d94-46d6-4164-928b-6426d06e903b
  Args:
    source: :Armin
    type: :Man
  AssignClass (ef7a4ffc-138f-4701-93dc-af2eccffa6b1)
 Call ID: ef7a4ffc-138f-4701-93dc-af2eccffa6b1
  Args:
    type: :Person
    source: :Armin
  AddTriple (aa5d3a11-b276-4eb9-8944-b486a4315f36)
 Call ID: aa5d3a11-b276-4eb9-8944-b486a4315f36
  Args:
    relation: :hasSon
    source: :Leopold_IV_Prince_of_Lippe
    target: :Armin
  AssignClass (fd211ded-7d7e-4ab6-9270-75b67a701ad2)
 Call ID: fd211ded-7d7e-4ab6-9270-75b67a701ad2
  Args:
    type: :Man
    source: :Bernhard_of_Biesterfeld
  AssignClass (66697a8b-5f65-4fa7-99c8-6ade297b5be3)
 Call ID: 66697a8b-5f65-4fa7-99c8-6ade297b5be3
  Args:
    source: :Bernhard_of_Biesterfeld
    type: :Person
  AssignClass (97a45e2c-05ee-4f81-9d15-9bf17cff1ca3)
 Call ID: 97a45e2c-05ee-4f81-9d15-9bf17cff1ca3
  Args:
    type: :Man
    source: :Bernhard_father_of_Bernhard_of_Biesterfeld
  AssignClass (07db5a5b-6192-4325-bcc1-5d83f3ec30f7)
 Call ID: 07db5a5b-6192-4325-bcc1-5d83f3ec30f7
  Args:
    type: :Person
    source: :Bernhard_father_of_Bernhard_of_Biesterfeld
  AddTriple (a15099bb-3992-4fb1-b44e-55afa5e38c75)
 Call ID: a15099bb-3992-4fb1-b44e-55afa5e38c75
  Args:
    target: :Bernhard_father_of_Bernhard_of_Biesterfeld
    source: :Leopold_IV_Prince_of_Lippe
    relation: :hasBrother
  AddTriple (1ad02183-d5e5-4e1b-a0da-29e84ba285ec)
 Call ID: 1ad02183-d5e5-4e1b-a0da-29e84ba285ec
  Args:
    source: :Bernhard_father_of_Bernhard_of_Biesterfeld
    target: :Bernhard_of_Biesterfeld
    relation: :hasSon
  Finish (53ec2c39-639e-4f32-8844-71fe0bf0ffe6)
 Call ID: 53ec2c39-639e-4f32-8844-71fe0bf0ffe6
  Args: