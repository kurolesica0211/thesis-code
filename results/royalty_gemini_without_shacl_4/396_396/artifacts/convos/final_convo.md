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
Princess Christina Margarethe of Hesse (German: Christina Margarethe Prinzessin von Hessen; 10 January 1933 – 22 November 2011) was a German princess.
Family background and early life

Born in Germany on 10 January 1933 at Friedrichshof Castle near Kronberg im Taunus, Princess Christina ("Krista") of Hesse was the eldest child of Prince Christoph of Hesse (1901–1943) and Princess Sophie of Greece and Denmark (1914–2001)
Her father, Prince Christoph of Hesse, was a nephew of Germany's last emperor Wilhelm II.
Her mother, Princess Sophie of Greece and Denmark, was a grand-daughter of King George I of Greece and a sister of Prince Philip, Duke of Edinburgh.
Christina belonged by birth to the senior line of the House of Hesse, a junior branch of which reigned as grand dukes of Hesse and by Rhine within the German Empire until 1918.
Christina's paternal grandmother, Princess Margaret of Prussia, was a daughter of Queen Victoria's eldest daughter Victoria, and as such a sister of Kaiser Wilhelm II.


Prince Christoph, a member of the Schutzstaffel (SS), held important positions in Germany's Nazi regime.
On 7 October 1943, when Christina was ten years old, her father was killed in an airplane crash in the Apennine Mountains near Forlì, Italy.
His widow married Prince George William of Hanover in 1946.
From her mother's two marriages, Christina had four siblings and three half-siblings: Princess Dorothea of Hesse (1934–2025), Prince Karl of Hesse (1937–2022), Prince Rainer of Hesse (born 1939), Princess Clarissa of Hesse (born 1944), Prince Welf of Hanover (1947–1981), Prince Georg of Hanover (born 1949) and Princess Friederike of Hanover (born 1954).
Her childhood homes included her paternal grandmother's palace of Friedrichshof in Taunus, a family castle at Panker in Holstein, and her parents' residence in Berlin-Dahlem.
Christina participated in the 1953 coronation of her aunt at Westminster Abbey, walking in the procession led by her maternal grandmother, Princess Alice.
Christina and her cousin Princess Beatrix of Hohenlohe-Langenburg spent the winter of 1955-1956 living in London, where Christina studied the restoration of paintings under Anthony Blunt.
It was reported that the princesses' closest friend in England was Prince Andrew of Yugoslavia.
First marriage

Princess Christina of Hesse married Prince Andrew of Yugoslavia, the youngest son of Alexander I of Yugoslavia and Princess Maria of Romania, on 2 August 1956, at Friedrichshof Castle.
They had two children:


Soon after their marriage, Princess Christina and her first husband had purchased The Hollands, a commercial farm at Langton Green in Kent, England, which did not prove a profitable venture.
Moving to London, Prince Andrew supported his family by working for an import/export business and, later, as a bank executive.
In 1961 Christina left her husband to live with an abstract artist from the Netherlands, Robert Floris van Eyck.
Second marriage

Following her divorce, Christina married Robert van Eyck on 3 December 1962 in London.
Her first husband Prince Andrew also married for the second time, this time to another cousin, Princess Kira Melita zu Leiningen (1930–2006).
Christina and Robert van Eyck separated in 1985, and divorced 3 February 1986.
In addition to Germany and England, Princess Christina of Hesse had lived in Saint-Paul-de-Vence, France, and in Gersau, Switzerland.



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
  AssignClass (5fa58389-9bcc-427c-ab99-40633b2559dd)
 Call ID: 5fa58389-9bcc-427c-ab99-40633b2559dd
  Args:
    source: Christina_Margarethe_of_Hesse
    type: :Woman
  AssignClass (a8ebe8d1-bdca-4da7-b952-4f2c68132bc3)
 Call ID: a8ebe8d1-bdca-4da7-b952-4f2c68132bc3
  Args:
    source: Christina_Margarethe_of_Hesse
    type: :Person
  AddLiteral (3833b0ae-e095-4392-a357-d3e965c1e792)
 Call ID: 3833b0ae-e095-4392-a357-d3e965c1e792
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1933
    source: Christina_Margarethe_of_Hesse
  AddLiteral (3a49b3ad-cabd-444e-8b01-fc639525c60e)
 Call ID: 3a49b3ad-cabd-444e-8b01-fc639525c60e
  Args:
    source: Christina_Margarethe_of_Hesse
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2011
  AssignClass (7cc16d6d-05b4-48e7-a78b-682c6993071f)
 Call ID: 7cc16d6d-05b4-48e7-a78b-682c6993071f
  Args:
    source: Christoph_of_Hesse
    type: :Man
  AssignClass (8529e979-13f9-4889-86d8-87162e794529)
 Call ID: 8529e979-13f9-4889-86d8-87162e794529
  Args:
    type: :Person
    source: Christoph_of_Hesse
  AssignClass (61f8bdb6-d48a-43a2-a76d-6673a9436562)
 Call ID: 61f8bdb6-d48a-43a2-a76d-6673a9436562
  Args:
    source: Christoph_of_Hesse
    type: :Ancestor
  AddLiteral (89876e7e-3cfd-414e-8c7a-f836702bcc34)
 Call ID: 89876e7e-3cfd-414e-8c7a-f836702bcc34
  Args:
    literal_value: 1901
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Christoph_of_Hesse
  AddLiteral (fc3e6a74-7b6b-4d50-b0f4-6220a69158f3)
 Call ID: fc3e6a74-7b6b-4d50-b0f4-6220a69158f3
  Args:
    literal_value: 1943
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Christoph_of_Hesse
  AssignClass (34250751-6d15-4688-8dc9-3bb5aabb55b2)
 Call ID: 34250751-6d15-4688-8dc9-3bb5aabb55b2
  Args:
    source: Sophie_of_Greece_and_Denmark
    type: :Woman
  AssignClass (e4f82c71-dd53-4bca-ac98-b551769e0a9b)
 Call ID: e4f82c71-dd53-4bca-ac98-b551769e0a9b
  Args:
    source: Sophie_of_Greece_and_Denmark
    type: :Person
  AssignClass (faccc459-a9c0-48a4-9320-38f8b0e5cceb)
 Call ID: faccc459-a9c0-48a4-9320-38f8b0e5cceb
  Args:
    source: Sophie_of_Greece_and_Denmark
    type: :Ancestor
  AddLiteral (8d6e201d-d57c-4fdc-aa88-d60ba80571e6)
 Call ID: 8d6e201d-d57c-4fdc-aa88-d60ba80571e6
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1914
    source: Sophie_of_Greece_and_Denmark
  AddLiteral (1b9da17e-b682-4d8b-bedf-dde5348267d5)
 Call ID: 1b9da17e-b682-4d8b-bedf-dde5348267d5
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2001
    source: Sophie_of_Greece_and_Denmark
  AddTriple (ab66124e-5305-42e8-9ab2-bbfe50a9dab2)
 Call ID: ab66124e-5305-42e8-9ab2-bbfe50a9dab2
  Args:
    relation: :hasFather
    target: Christoph_of_Hesse
    source: Christina_Margarethe_of_Hesse
  AddTriple (89ae03ae-c205-44dd-bb3c-66188ffc523f)
 Call ID: 89ae03ae-c205-44dd-bb3c-66188ffc523f
  Args:
    source: Christina_Margarethe_of_Hesse
    target: Sophie_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (3117a2e3-6dd8-48e2-b9e2-62c6cca45514)
 Call ID: 3117a2e3-6dd8-48e2-b9e2-62c6cca45514
  Args:
    type: :Woman
    source: Dorothea_of_Hesse
  AssignClass (7d36731a-4d41-49b2-9f02-aaa27ac1f143)
 Call ID: 7d36731a-4d41-49b2-9f02-aaa27ac1f143
  Args:
    source: Dorothea_of_Hesse
    type: :Person
  AddTriple (af6bdef0-7267-43a6-81a6-72528fb84f34)
 Call ID: af6bdef0-7267-43a6-81a6-72528fb84f34
  Args:
    target: Dorothea_of_Hesse
    relation: :isSiblingOf
    source: Christina_Margarethe_of_Hesse
  AssignClass (2a26be52-b886-4f98-82d1-647878b2a8f9)
 Call ID: 2a26be52-b886-4f98-82d1-647878b2a8f9
  Args:
    type: :Man
    source: Karl_of_Hesse
  AssignClass (1bd43edf-cf0c-4f82-b7f1-7e190eae2ffe)
 Call ID: 1bd43edf-cf0c-4f82-b7f1-7e190eae2ffe
  Args:
    type: :Person
    source: Karl_of_Hesse
  AddTriple (02192338-cd71-4b3a-a135-c44d868129b7)
 Call ID: 02192338-cd71-4b3a-a135-c44d868129b7
  Args:
    source: Christina_Margarethe_of_Hesse
    relation: :isSiblingOf
    target: Karl_of_Hesse
  AssignClass (22848d36-fceb-4fac-9ff6-e156d2077a05)
 Call ID: 22848d36-fceb-4fac-9ff6-e156d2077a05
  Args:
    type: :Man
    source: Rainer_of_Hesse
  AssignClass (9aeb1e90-7210-4356-8c28-0471bef41c37)
 Call ID: 9aeb1e90-7210-4356-8c28-0471bef41c37
  Args:
    type: :Person
    source: Rainer_of_Hesse
  AddTriple (1e65202d-a028-4734-85d9-eb82a86a6b7d)
 Call ID: 1e65202d-a028-4734-85d9-eb82a86a6b7d
  Args:
    source: Christina_Margarethe_of_Hesse
    target: Rainer_of_Hesse
    relation: :isSiblingOf
  AssignClass (96da2078-ae1a-4103-8d6f-c5a1e1c37edb)
 Call ID: 96da2078-ae1a-4103-8d6f-c5a1e1c37edb
  Args:
    type: :Woman
    source: Clarissa_of_Hesse
  AssignClass (a748437f-c1f3-4fb3-8303-946a8cb7a705)
 Call ID: a748437f-c1f3-4fb3-8303-946a8cb7a705
  Args:
    type: :Person
    source: Clarissa_of_Hesse
  AddTriple (d2c1a360-e51f-476e-9233-73a9442e681b)
 Call ID: d2c1a360-e51f-476e-9233-73a9442e681b
  Args:
    source: Christina_Margarethe_of_Hesse
    target: Clarissa_of_Hesse
    relation: :isSiblingOf
  AssignClass (6f50f7ce-261d-4b79-bccc-65c7421223cc)
 Call ID: 6f50f7ce-261d-4b79-bccc-65c7421223cc
  Args:
    type: :Man
    source: Welf_of_Hanover
  AssignClass (8ee6e03c-ff5a-4165-aaea-8ca05dc886f1)
 Call ID: 8ee6e03c-ff5a-4165-aaea-8ca05dc886f1
  Args:
    source: Welf_of_Hanover
    type: :Person
  AddTriple (3cccc575-738d-4619-ae79-537cae41c441)
 Call ID: 3cccc575-738d-4619-ae79-537cae41c441
  Args:
    source: Christina_Margarethe_of_Hesse
    target: Welf_of_Hanover
    relation: :isSiblingOf
  AssignClass (77ecd67e-bd4d-4686-8092-ea3654dba3cd)
 Call ID: 77ecd67e-bd4d-4686-8092-ea3654dba3cd
  Args:
    type: :Man
    source: Georg_of_Hanover
  AssignClass (95b71d03-3b6c-4704-ad84-9846dfc44c1b)
 Call ID: 95b71d03-3b6c-4704-ad84-9846dfc44c1b
  Args:
    type: :Person
    source: Georg_of_Hanover
  AddTriple (84f77aca-75a9-497c-b815-17d6f07393cb)
 Call ID: 84f77aca-75a9-497c-b815-17d6f07393cb
  Args:
    relation: :isSiblingOf
    target: Georg_of_Hanover
    source: Christina_Margarethe_of_Hesse
  AssignClass (5734ae65-bf1a-4aae-a4a5-dee96a63f322)
 Call ID: 5734ae65-bf1a-4aae-a4a5-dee96a63f322
  Args:
    type: :Woman
    source: Friederike_of_Hanover
  AssignClass (2164fb01-c33c-4c85-b6e7-d3e3fee7642a)
 Call ID: 2164fb01-c33c-4c85-b6e7-d3e3fee7642a
  Args:
    type: :Person
    source: Friederike_of_Hanover
  AddTriple (c776a9bb-202e-4094-876c-9ff76cab2de9)
 Call ID: c776a9bb-202e-4094-876c-9ff76cab2de9
  Args:
    target: Friederike_of_Hanover
    relation: :isSiblingOf
    source: Christina_Margarethe_of_Hesse
  AssignClass (60632486-0d16-4a2e-90e5-8637f72a4cf5)
 Call ID: 60632486-0d16-4a2e-90e5-8637f72a4cf5
  Args:
    type: :Man
    source: Andrew_of_Yugoslavia
  AssignClass (aa673032-0962-41e1-bfce-12f363a57052)
 Call ID: aa673032-0962-41e1-bfce-12f363a57052
  Args:
    source: Andrew_of_Yugoslavia
    type: :Person
  AddTriple (d1ab0535-e557-4186-a71f-e7f3cecf6736)
 Call ID: d1ab0535-e557-4186-a71f-e7f3cecf6736
  Args:
    source: Christina_Margarethe_of_Hesse
    relation: :hasRelation
    target: Andrew_of_Yugoslavia
  AddLiteral (01a4ccda-0ee3-49de-bc14-736d457450d2)
 Call ID: 01a4ccda-0ee3-49de-bc14-736d457450d2
  Args:
    source: Christina_Margarethe_of_Hesse
    literal_value: 1956
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (175b17e7-6061-4997-a0ef-93c25185d173)
 Call ID: 175b17e7-6061-4997-a0ef-93c25185d173
  Args:
    type: :Man
    source: Robert_van_Eyck
  AssignClass (82ab1752-5571-476f-81c5-a4aa1aca5498)
 Call ID: 82ab1752-5571-476f-81c5-a4aa1aca5498
  Args:
    type: :Person
    source: Robert_van_Eyck
  AddTriple (4f1c4c8d-b99c-4776-8510-609b7f4a8cc0)
 Call ID: 4f1c4c8d-b99c-4776-8510-609b7f4a8cc0
  Args:
    target: Robert_van_Eyck
    relation: :hasRelation
    source: Christina_Margarethe_of_Hesse
  AddLiteral (e31ad7cb-f737-47bb-87d7-3058a62b971c)
 Call ID: e31ad7cb-f737-47bb-87d7-3058a62b971c
  Args:
    literal_value: 1962
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Christina_Margarethe_of_Hesse
  Finish (ae2f67cc-4d04-44ee-bd2f-e6d00b78225e)
 Call ID: ae2f67cc-4d04-44ee-bd2f-e6d00b78225e
  Args: