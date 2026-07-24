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
Princess Alexandra of Sayn-Wittgenstein-Berleburg, Countess Ahlefeldt-Laurvig-Bille (Alexandra Rosemarie Ingrid Benedikte; born 20 November 1970), is the first daughter and second of three children of Prince Richard of Sayn-Wittgenstein-Berleburg and Princess Benedikte of Denmark, sister of two Queens, Margrethe II and Anne-Marie of Greece.
She is the first cousin of King Frederik X of Denmark.
Succession rights in Denmark

Under the succession rules set by King Frederik IX, since Princess Benedikte and her children, Prince Gustav, Princess Nathalie and Princess Alexandra, have not taken up permanent residence in Denmark, they have effectively waived their place in the line of succession to the Danish throne.
Since 19 May 1998, Alexandra has been a Danish citizen.
First marriage and children

Alexandra was married on 6 June 1998 at Gråsten Palace to Count Jefferson von Pfeil und Klein-Ellguth.
Jefferson and Alexandra are distantly related, both descending from Leopold III, Duke of Anhalt-Dessau.
Beginning in 2013, Alexandra and Jefferson lived in Heidesheim Castle, Germany, near Mainz.
Second marriage

On 18 May 2019, Alexandra married Count Michael of Ahlefeldt-Laurvig-Bille at Sankt Jørgens Kirke in Svendborgsund.
She has one sister-in-law, Countess Suzanne Ingrid Jessie Dorthe Ahlefeldt-Laurvig-Bille (b. Svendborg, 4 March 1967), lady-in-waiting to Alexandra, Countess of Frederiksborg, who married her third cousin once removed, Erik Ove Carl John Emil Vind til Sanderumgaard (b. Hellerup, 5 May 1954), the grandson of Prince Erik of Denmark.
They currently live at Egeskov Castle, ancestral home and a country residence of the Counts of Ahlefeldt, which is managed by Count Michael Preben, while Princess Alexandra engages herself in drawing, garden designing and art history.
Career

Princess Alexandra worked for UNESCO



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (9d3f32d7-12f3-44a1-944f-c2138d18a17b)
 Call ID: 9d3f32d7-12f3-44a1-944f-c2138d18a17b
  Args:
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    type: :Woman
  AssignClass (5cabc4eb-0ebc-45c9-ae89-dd8b74663059)
 Call ID: 5cabc4eb-0ebc-45c9-ae89-dd8b74663059
  Args:
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AddLiteral (e061c59a-d133-47b4-8da6-b862a73c2c89)
 Call ID: e061c59a-d133-47b4-8da6-b862a73c2c89
  Args:
    literal_type: xsd:integer
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    literal_value: 1970
    relation: :hasBirthYear
  AssignClass (40c06ef7-8591-4895-bf03-74b915b10fd7)
 Call ID: 40c06ef7-8591-4895-bf03-74b915b10fd7
  Args:
    source: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
    type: :Man
  AssignClass (03a098d4-df4d-4e9c-9062-59d6387b3281)
 Call ID: 03a098d4-df4d-4e9c-9062-59d6387b3281
  Args:
    source: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AssignClass (cff23742-22cd-4bc2-bc18-6a65703c0b0a)
 Call ID: cff23742-22cd-4bc2-bc18-6a65703c0b0a
  Args:
    type: :Woman
    source: Princess_Benedikte_of_Denmark
  AssignClass (d5a4c756-f101-439e-86e2-f32658961a58)
 Call ID: d5a4c756-f101-439e-86e2-f32658961a58
  Args:
    source: Princess_Benedikte_of_Denmark
    type: :Person
  AddTriple (64348d0b-90aa-4793-a51f-a4e5fcc5bd1c)
 Call ID: 64348d0b-90aa-4793-a51f-a4e5fcc5bd1c
  Args:
    relation: :hasFather
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    target: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
  AddTriple (0f07bd6f-6bf7-4729-b6f8-6693fdf0b6a2)
 Call ID: 0f07bd6f-6bf7-4729-b6f8-6693fdf0b6a2
  Args:
    relation: :hasMother
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    target: Princess_Benedikte_of_Denmark
  AssignClass (b0861845-7ad9-49a4-bc27-3afe369d48aa)
 Call ID: b0861845-7ad9-49a4-bc27-3afe369d48aa
  Args:
    type: :Man
    source: Prince_Gustav
  AssignClass (fb455f5b-0b05-4874-822b-0ab289eaadc0)
 Call ID: fb455f5b-0b05-4874-822b-0ab289eaadc0
  Args:
    source: Prince_Gustav
    type: :Person
  AssignClass (705de486-99d5-426d-8499-d340d2957508)
 Call ID: 705de486-99d5-426d-8499-d340d2957508
  Args:
    type: :Woman
    source: Princess_Nathalie
  AssignClass (45ad23f2-6f45-440d-ac6c-4e4645d2d1df)
 Call ID: 45ad23f2-6f45-440d-ac6c-4e4645d2d1df
  Args:
    source: Princess_Nathalie
    type: :Person
  AddTriple (bf7a2470-1dd1-4ea4-baf3-4c9ee235f314)
 Call ID: bf7a2470-1dd1-4ea4-baf3-4c9ee235f314
  Args:
    relation: :hasFather
    source: Prince_Gustav
    target: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
  AddTriple (3cc4a2ef-5b93-458c-8bf5-379cb3b4beaf)
 Call ID: 3cc4a2ef-5b93-458c-8bf5-379cb3b4beaf
  Args:
    relation: :hasMother
    source: Prince_Gustav
    target: Princess_Benedikte_of_Denmark
  AddTriple (a79101a9-7420-49c3-a238-386fe7a7a40f)
 Call ID: a79101a9-7420-49c3-a238-386fe7a7a40f
  Args:
    relation: :hasFather
    source: Princess_Nathalie
    target: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
  AddTriple (c9aa42a8-8e96-495d-b6bf-6a8003da6e88)
 Call ID: c9aa42a8-8e96-495d-b6bf-6a8003da6e88
  Args:
    relation: :hasMother
    source: Princess_Nathalie
    target: Princess_Benedikte_of_Denmark
  AssignClass (65ecacb7-0ddd-4e46-9693-cebd3c42d011)
 Call ID: 65ecacb7-0ddd-4e46-9693-cebd3c42d011
  Args:
    source: Count_Jefferson_von_Pfeil_und_Klein-Ellguth
    type: :Man
  AssignClass (fdbfebe0-c73a-4eaa-851f-ae0aaf379797)
 Call ID: fdbfebe0-c73a-4eaa-851f-ae0aaf379797
  Args:
    type: :Person
    source: Count_Jefferson_von_Pfeil_und_Klein-Ellguth
  AddLiteral (3de92cb3-990f-498d-baaa-c90cd6ed0387)
 Call ID: 3de92cb3-990f-498d-baaa-c90cd6ed0387
  Args:
    relation: :hasMarriageYear
    literal_value: 1998
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    literal_type: xsd:integer
  AssignClass (7001a9b7-8056-4767-979a-486ba8a20626)
 Call ID: 7001a9b7-8056-4767-979a-486ba8a20626
  Args:
    type: :Man
    source: Count_Michael_of_Ahlefeldt-Laurvig-Bille
  AssignClass (87a07a2e-6c1e-4d3b-a638-3970e152bb91)
 Call ID: 87a07a2e-6c1e-4d3b-a638-3970e152bb91
  Args:
    type: :Person
    source: Count_Michael_of_Ahlefeldt-Laurvig-Bille
  AddLiteral (a449ea00-f3ef-4f19-b159-29fa9c3bcf6a)
 Call ID: a449ea00-f3ef-4f19-b159-29fa9c3bcf6a
  Args:
    relation: :hasMarriageYear
    literal_value: 2019
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    literal_type: xsd:integer
  AssignClass (081db465-09ea-4b7f-b38d-bef8ad2d28b1)
 Call ID: 081db465-09ea-4b7f-b38d-bef8ad2d28b1
  Args:
    source: Countess_Suzanne_Ingrid_Jessie_Dorthe_Ahlefeldt-Laurvig-Bille
    type: :Woman
  AssignClass (0f1750a4-1988-4ad9-90c3-e83c7380d365)
 Call ID: 0f1750a4-1988-4ad9-90c3-e83c7380d365
  Args:
    type: :Person
    source: Countess_Suzanne_Ingrid_Jessie_Dorthe_Ahlefeldt-Laurvig-Bille
  AssignClass (6fd4dbfc-476a-4969-9172-4657bda7ea16)
 Call ID: 6fd4dbfc-476a-4969-9172-4657bda7ea16
  Args:
    type: :Man
    source: Erik_Ove_Carl_John_Emil_Vind_til_Sanderumgaard
  AssignClass (247ddcf4-cd71-4448-90e6-f00cdc0af573)
 Call ID: 247ddcf4-cd71-4448-90e6-f00cdc0af573
  Args:
    source: Erik_Ove_Carl_John_Emil_Vind_til_Sanderumgaard
    type: :Person
  Finish (b4db7c3b-2d18-4a3d-8008-bfb49469e08d)
 Call ID: b4db7c3b-2d18-4a3d-8008-bfb49469e08d
  Args: