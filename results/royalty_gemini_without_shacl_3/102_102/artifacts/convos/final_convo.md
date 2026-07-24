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
  AssignClass (870275b0-729d-47d8-afae-902f8a3c5d5c)
 Call ID: 870275b0-729d-47d8-afae-902f8a3c5d5c
  Args:
    type: :Woman
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AssignClass (1ee992f3-34ea-4546-a60e-cf52a2a4dc78)
 Call ID: 1ee992f3-34ea-4546-a60e-cf52a2a4dc78
  Args:
    type: :Man
    source: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
  AssignClass (c12b059c-7004-4956-a532-9a6084195eee)
 Call ID: c12b059c-7004-4956-a532-9a6084195eee
  Args:
    type: :Woman
    source: Princess_Benedikte_of_Denmark
  AddLiteral (d84e3559-ef55-4586-b578-ba8341c2e641)
 Call ID: d84e3559-ef55-4586-b578-ba8341c2e641
  Args:
    literal_value: 1970
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AddTriple (f7c52a8d-83b0-445f-8a89-3876eb248bdb)
 Call ID: f7c52a8d-83b0-445f-8a89-3876eb248bdb
  Args:
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    relation: :hasFather
    target: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
  AddTriple (a7a1cc37-0b8e-4d23-b9b0-dd037448d70c)
 Call ID: a7a1cc37-0b8e-4d23-b9b0-dd037448d70c
  Args:
    target: Princess_Benedikte_of_Denmark
    relation: :hasMother
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AssignClass (8883cfb6-c59c-4df1-8a54-9a8a40c4f547)
 Call ID: 8883cfb6-c59c-4df1-8a54-9a8a40c4f547
  Args:
    type: :Man
    source: Prince_Gustav
  AssignClass (482d599a-c890-44b3-b654-35165d4f4dd2)
 Call ID: 482d599a-c890-44b3-b654-35165d4f4dd2
  Args:
    type: :Woman
    source: Princess_Nathalie
  AddTriple (56d8fae0-7c45-479d-bbda-3d4b15126716)
 Call ID: 56d8fae0-7c45-479d-bbda-3d4b15126716
  Args:
    source: Prince_Gustav
    target: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
    relation: :hasParent
  AddTriple (ff011272-a747-434e-b4ac-9c044b0ee087)
 Call ID: ff011272-a747-434e-b4ac-9c044b0ee087
  Args:
    target: Princess_Benedikte_of_Denmark
    relation: :hasParent
    source: Prince_Gustav
  AddTriple (a5991f05-5f8a-45c3-9e04-0ae57b5290f7)
 Call ID: a5991f05-5f8a-45c3-9e04-0ae57b5290f7
  Args:
    source: Princess_Nathalie
    target: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
    relation: :hasParent
  AddTriple (243edb49-88f8-4023-8cde-484f65d49e41)
 Call ID: 243edb49-88f8-4023-8cde-484f65d49e41
  Args:
    target: Princess_Benedikte_of_Denmark
    relation: :hasParent
    source: Princess_Nathalie
  AddTriple (e2b9cc8a-2612-49ab-8b5f-94e8cab733c1)
 Call ID: e2b9cc8a-2612-49ab-8b5f-94e8cab733c1
  Args:
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    target: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
    relation: :hasParent
  AddTriple (c1ec9a8a-a839-4c1d-9c67-5b83d68b2583)
 Call ID: c1ec9a8a-a839-4c1d-9c67-5b83d68b2583
  Args:
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    relation: :hasParent
    target: Princess_Benedikte_of_Denmark
  AssignClass (49c2af89-63dc-4170-915d-d0335f5d6e29)
 Call ID: 49c2af89-63dc-4170-915d-d0335f5d6e29
  Args:
    type: :Man
    source: Count_Jefferson_von_Pfeil_und_Klein-Ellguth
  AddTriple (96264ab3-3559-4cf4-897b-dd354d0ccfd7)
 Call ID: 96264ab3-3559-4cf4-897b-dd354d0ccfd7
  Args:
    relation: :hasRelation
    target: Count_Jefferson_von_Pfeil_und_Klein-Ellguth
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AddLiteral (3383ffe5-aabf-47f3-abc6-7a1572c81602)
 Call ID: 3383ffe5-aabf-47f3-abc6-7a1572c81602
  Args:
    literal_type: xsd:integer
    literal_value: 1998
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    relation: :hasMarriageYear
  AssignClass (5ff049a5-41c3-4ed9-898e-758b0bb02f72)
 Call ID: 5ff049a5-41c3-4ed9-898e-758b0bb02f72
  Args:
    type: :Man
    source: Count_Michael_of_Ahlefeldt-Laurvig-Bille
  AddTriple (d8ea3832-3934-495f-86ff-0d019b4f88db)
 Call ID: d8ea3832-3934-495f-86ff-0d019b4f88db
  Args:
    target: Count_Michael_of_Ahlefeldt-Laurvig-Bille
    relation: :hasRelation
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AddLiteral (8f056a08-313e-4254-a2be-7dd9e22f7c06)
 Call ID: 8f056a08-313e-4254-a2be-7dd9e22f7c06
  Args:
    literal_type: xsd:integer
    literal_value: 2019
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    relation: :hasMarriageYear
  Finish (44adde1c-4ebf-4a48-a61b-5fb103fe37f7)
 Call ID: 44adde1c-4ebf-4a48-a61b-5fb103fe37f7
  Args: