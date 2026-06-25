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
  AssignClass (1742b181-fa16-4437-bb04-ebc0ca2bbdc9)
 Call ID: 1742b181-fa16-4437-bb04-ebc0ca2bbdc9
  Args:
    type: :Woman
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AssignClass (55d73835-1de7-4ea2-bbe3-1eb0c851173f)
 Call ID: 55d73835-1de7-4ea2-bbe3-1eb0c851173f
  Args:
    type: :Person
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AddLiteral (f32e1f55-e0f1-4120-8cb1-5de72061c729)
 Call ID: f32e1f55-e0f1-4120-8cb1-5de72061c729
  Args:
    literal_value: 1970
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (fccc5589-e930-47c6-aee7-ef56116ec18e)
 Call ID: fccc5589-e930-47c6-aee7-ef56116ec18e
  Args:
    type: :Man
    source: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
  AssignClass (c9a86891-8f10-40c4-a522-22eb39c06dd3)
 Call ID: c9a86891-8f10-40c4-a522-22eb39c06dd3
  Args:
    source: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AssignClass (c5a89dce-f771-4de3-acf9-0dfb838cb723)
 Call ID: c5a89dce-f771-4de3-acf9-0dfb838cb723
  Args:
    source: Princess_Benedikte_of_Denmark
    type: :Woman
  AssignClass (a1055afe-0618-4d2a-8682-a0019658d0a5)
 Call ID: a1055afe-0618-4d2a-8682-a0019658d0a5
  Args:
    source: Princess_Benedikte_of_Denmark
    type: :Person
  AddTriple (54df6e8a-62c8-449f-aaa6-afa51c696ab0)
 Call ID: 54df6e8a-62c8-449f-aaa6-afa51c696ab0
  Args:
    relation: :hasFather
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    target: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
  AddTriple (7704fc1b-b633-4e10-a467-cbaa12302dd1)
 Call ID: 7704fc1b-b633-4e10-a467-cbaa12302dd1
  Args:
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    target: Princess_Benedikte_of_Denmark
    relation: :hasMother
  AssignClass (a5306ffe-965a-456c-ae38-edd2c878a1fc)
 Call ID: a5306ffe-965a-456c-ae38-edd2c878a1fc
  Args:
    type: :Man
    source: Prince_Gustav
  AssignClass (e4d8e2c6-5271-448e-bc49-6558211dfbf1)
 Call ID: e4d8e2c6-5271-448e-bc49-6558211dfbf1
  Args:
    type: :Person
    source: Prince_Gustav
  AssignClass (fc0731a9-ff8f-4938-9151-a77091bc761e)
 Call ID: fc0731a9-ff8f-4938-9151-a77091bc761e
  Args:
    type: :Woman
    source: Princess_Nathalie
  AssignClass (e92b9060-3d5f-42bd-a09b-77ec09dfab46)
 Call ID: e92b9060-3d5f-42bd-a09b-77ec09dfab46
  Args:
    source: Princess_Nathalie
    type: :Person
  AddTriple (a27a162b-49fe-46cb-ba06-42ac8163584a)
 Call ID: a27a162b-49fe-46cb-ba06-42ac8163584a
  Args:
    target: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
    source: Prince_Gustav
    relation: :hasFather
  AddTriple (1e40f962-2761-4044-8f2a-6c61c754d127)
 Call ID: 1e40f962-2761-4044-8f2a-6c61c754d127
  Args:
    target: Princess_Benedikte_of_Denmark
    source: Prince_Gustav
    relation: :hasMother
  AddTriple (2b03b2e0-1de8-47ee-80bd-2aedc491f622)
 Call ID: 2b03b2e0-1de8-47ee-80bd-2aedc491f622
  Args:
    source: Princess_Nathalie
    target: Prince_Richard_of_Sayn-Wittgenstein-Berleburg
    relation: :hasFather
  AddTriple (7f37c2a9-4161-46d0-8779-c4631fb7cf8e)
 Call ID: 7f37c2a9-4161-46d0-8779-c4631fb7cf8e
  Args:
    target: Princess_Benedikte_of_Denmark
    source: Princess_Nathalie
    relation: :hasMother
  AssignClass (f2dbd616-d36b-4261-ac02-9527f828a22c)
 Call ID: f2dbd616-d36b-4261-ac02-9527f828a22c
  Args:
    source: Count_Jefferson_von_Pfeil_und_Klein-Ellguth
    type: :Man
  AssignClass (db647202-cca7-499c-aca0-944bf1b50dfb)
 Call ID: db647202-cca7-499c-aca0-944bf1b50dfb
  Args:
    type: :Person
    source: Count_Jefferson_von_Pfeil_und_Klein-Ellguth
  AddLiteral (3b97cbf7-f8bb-407a-b10b-213dcf4795b6)
 Call ID: 3b97cbf7-f8bb-407a-b10b-213dcf4795b6
  Args:
    literal_value: 1998
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (0209d122-48b4-412d-a8e0-1a2617b61d67)
 Call ID: 0209d122-48b4-412d-a8e0-1a2617b61d67
  Args:
    relation: :hasRelation
    target: Count_Jefferson_von_Pfeil_und_Klein-Ellguth
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AssignClass (d97fca34-0f6d-429d-bebd-ca34bf59763f)
 Call ID: d97fca34-0f6d-429d-bebd-ca34bf59763f
  Args:
    type: :Man
    source: Count_Michael_of_Ahlefeldt-Laurvig-Bille
  AssignClass (3625d7ec-380d-4fdb-b08f-ce902340ac05)
 Call ID: 3625d7ec-380d-4fdb-b08f-ce902340ac05
  Args:
    type: :Person
    source: Count_Michael_of_Ahlefeldt-Laurvig-Bille
  AddLiteral (307515b6-1aca-43c4-b7dc-c2f961661fd4)
 Call ID: 307515b6-1aca-43c4-b7dc-c2f961661fd4
  Args:
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    literal_value: 2019
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (52c9c219-c429-4dd7-aeb4-4de881208884)
 Call ID: 52c9c219-c429-4dd7-aeb4-4de881208884
  Args:
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    target: Count_Michael_of_Ahlefeldt-Laurvig-Bille
    relation: :hasRelation
  AssignClass (8acc692a-c775-4f97-b2d5-2d38f125a40f)
 Call ID: 8acc692a-c775-4f97-b2d5-2d38f125a40f
  Args:
    type: :Woman
    source: Countess_Suzanne_Ingrid_Jessie_Dorthe_Ahlefeldt-Laurvig-Bille
  AssignClass (a328536e-73ee-425a-960b-6fabc1708928)
 Call ID: a328536e-73ee-425a-960b-6fabc1708928
  Args:
    source: Countess_Suzanne_Ingrid_Jessie_Dorthe_Ahlefeldt-Laurvig-Bille
    type: :Person
  AssignClass (240d984c-f387-45c4-a659-2ea6272c734a)
 Call ID: 240d984c-f387-45c4-a659-2ea6272c734a
  Args:
    source: Erik_Ove_Carl_John_Emil_Vind_til_Sanderumgaard
    type: :Man
  AssignClass (c27ad9bb-5892-4633-a7db-d211bfddaf99)
 Call ID: c27ad9bb-5892-4633-a7db-d211bfddaf99
  Args:
    type: :Person
    source: Erik_Ove_Carl_John_Emil_Vind_til_Sanderumgaard
  AddTriple (23b40571-7269-470c-8102-e7adb66564d3)
 Call ID: 23b40571-7269-470c-8102-e7adb66564d3
  Args:
    target: Erik_Ove_Carl_John_Emil_Vind_til_Sanderumgaard
    source: Countess_Suzanne_Ingrid_Jessie_Dorthe_Ahlefeldt-Laurvig-Bille
    relation: :hasRelation
  Finish (678a1443-c442-43fa-813e-59f4d4621769)
 Call ID: 678a1443-c442-43fa-813e-59f4d4621769
  Args: