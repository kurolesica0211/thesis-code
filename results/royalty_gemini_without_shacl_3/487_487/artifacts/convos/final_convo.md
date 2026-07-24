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
Eleonore von Habsburg-Lothringen (Eleonore Maria del Pilar Iona Christina Jelena; born 28 February 1994) is an Austrian jewellery designer, gemologist, and model.
She is the daughter of Karl von Habsburg, the head of the House of Habsburg-Lorraine.
Early life and background

Eleonore Habsburg-Lorraine was born in 1994 in Salzburg to Karl von Habsburg, a politician and head of the House of Habsburg-Lorraine, and Francesca von Thyssen-Bornemisza de Kászon et Impérfalva, an art collector and by birth member of the Thyssen-Bornemisza family.
Her paternal grandparents were Otto, Crown Prince of Austria and Princess Regina of Saxe-Meiningen.
Her paternal great-grandparents Charles I of Austria and Zita of Bourbon-Parma were the last Emperor and Empress of Austria.
Her brother is racing car driver Ferdinand Habsburg.
Education and career

Habsburg-Lorraine attended boarding school in Gstaad before studying law at the European Business School London.
Habsburg has also worked as a fashion model, being featured in advertisement campaigns and walking the runway for Dolce & Gabbana.
Personal life

On 20 July 2020, Eleonore von Habsburg-Lorraine married Belgian race car driver Jérôme d'Ambrosio in a small civil ceremony at the Civil Registry of Monaco, conducted by the Mayor of Monaco Georges Marsan.
On 20 October 2021 she gave birth to a son, Otto d'Ambrosio, named after her grandfather Otto von Habsburg.



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
  AssignClass (771deef8-1f52-4f56-b302-d19f62223684)
 Call ID: 771deef8-1f52-4f56-b302-d19f62223684
  Args:
    source: Eleonore_von_Habsburg-Lothringen
    type: :Person
  AssignClass (5f348701-c3e6-492e-9bc6-97af0a86faf6)
 Call ID: 5f348701-c3e6-492e-9bc6-97af0a86faf6
  Args:
    source: Eleonore_von_Habsburg-Lothringen
    type: :Woman
  AddLiteral (378c4672-d2f2-4330-9d17-ff63dafa97a9)
 Call ID: 378c4672-d2f2-4330-9d17-ff63dafa97a9
  Args:
    source: Eleonore_von_Habsburg-Lothringen
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1994
  AssignClass (39fdef74-2606-4ae5-8edf-a08949535a48)
 Call ID: 39fdef74-2606-4ae5-8edf-a08949535a48
  Args:
    source: Karl_von_Habsburg
    type: :Person
  AssignClass (5623e8bd-3d94-4de2-bbd9-2d589326c799)
 Call ID: 5623e8bd-3d94-4de2-bbd9-2d589326c799
  Args:
    type: :Man
    source: Karl_von_Habsburg
  AddTriple (c37ead76-6f12-48c0-afdf-b327eea204ac)
 Call ID: c37ead76-6f12-48c0-afdf-b327eea204ac
  Args:
    target: Karl_von_Habsburg
    source: Eleonore_von_Habsburg-Lothringen
    relation: :hasFather
  AssignClass (59f775a9-b098-45ad-949b-1d2c9b273b91)
 Call ID: 59f775a9-b098-45ad-949b-1d2c9b273b91
  Args:
    source: Francesca_von_Thyssen-Bornemisza
    type: :Person
  AssignClass (fe4407c0-2c13-4ff9-8d56-a0b3dc026a52)
 Call ID: fe4407c0-2c13-4ff9-8d56-a0b3dc026a52
  Args:
    source: Francesca_von_Thyssen-Bornemisza
    type: :Woman
  AddTriple (bd28e719-2e9b-4ede-a343-b92b46feefa1)
 Call ID: bd28e719-2e9b-4ede-a343-b92b46feefa1
  Args:
    source: Eleonore_von_Habsburg-Lothringen
    relation: :hasMother
    target: Francesca_von_Thyssen-Bornemisza
  AssignClass (71dbc1f8-3fde-4d17-8233-14618689dff2)
 Call ID: 71dbc1f8-3fde-4d17-8233-14618689dff2
  Args:
    type: :Person
    source: Otto_von_Habsburg
  AssignClass (6f99f195-952f-4b97-9546-55ee086bf025)
 Call ID: 6f99f195-952f-4b97-9546-55ee086bf025
  Args:
    type: :Man
    source: Otto_von_Habsburg
  AssignClass (b623a778-cd49-455c-9c08-fd7a9505aa8b)
 Call ID: b623a778-cd49-455c-9c08-fd7a9505aa8b
  Args:
    type: :Person
    source: Regina_von_Saxe-Meiningen
  AssignClass (e77e6678-ac62-4a40-8309-cea7262030dc)
 Call ID: e77e6678-ac62-4a40-8309-cea7262030dc
  Args:
    source: Regina_von_Saxe-Meiningen
    type: :Woman
  AddTriple (9ead31e7-71c1-452d-bc4f-346b46b24237)
 Call ID: 9ead31e7-71c1-452d-bc4f-346b46b24237
  Args:
    source: Karl_von_Habsburg
    relation: :hasFather
    target: Otto_von_Habsburg
  AddTriple (9832043c-521e-4018-9d2d-fcb10c2e8470)
 Call ID: 9832043c-521e-4018-9d2d-fcb10c2e8470
  Args:
    relation: :hasMother
    source: Karl_von_Habsburg
    target: Regina_von_Saxe-Meiningen
  AssignClass (58380c5e-5199-4107-b7b9-d26783fdc631)
 Call ID: 58380c5e-5199-4107-b7b9-d26783fdc631
  Args:
    type: :Person
    source: Charles_I_of_Austria
  AssignClass (07c522ff-2b9f-47c6-83a4-368cdd06bde0)
 Call ID: 07c522ff-2b9f-47c6-83a4-368cdd06bde0
  Args:
    type: :Man
    source: Charles_I_of_Austria
  AssignClass (7825196c-f6f8-4fbf-8bdf-b95efa2c1408)
 Call ID: 7825196c-f6f8-4fbf-8bdf-b95efa2c1408
  Args:
    type: :Person
    source: Zita_of_Bourbon-Parma
  AssignClass (db81cb94-6a42-4138-8e9d-2128aa40bd51)
 Call ID: db81cb94-6a42-4138-8e9d-2128aa40bd51
  Args:
    type: :Woman
    source: Zita_of_Bourbon-Parma
  AddTriple (93bb9b09-4f3a-4eb1-8a28-97e93f25c0c5)
 Call ID: 93bb9b09-4f3a-4eb1-8a28-97e93f25c0c5
  Args:
    relation: :hasFather
    source: Otto_von_Habsburg
    target: Charles_I_of_Austria
  AddTriple (0af824e3-90aa-4b2f-a1e3-1188f5764a0d)
 Call ID: 0af824e3-90aa-4b2f-a1e3-1188f5764a0d
  Args:
    target: Zita_of_Bourbon-Parma
    relation: :hasMother
    source: Otto_von_Habsburg
  AssignClass (940be255-62c2-47cf-9ecd-8ab443c81ccd)
 Call ID: 940be255-62c2-47cf-9ecd-8ab443c81ccd
  Args:
    type: :Person
    source: Ferdinand_Habsburg
  AssignClass (67d99e27-15f0-46fe-90f6-451afb69385a)
 Call ID: 67d99e27-15f0-46fe-90f6-451afb69385a
  Args:
    type: :Man
    source: Ferdinand_Habsburg
  AddTriple (03cca6fa-34e5-4f10-86d2-378d7274f580)
 Call ID: 03cca6fa-34e5-4f10-86d2-378d7274f580
  Args:
    relation: :hasBrother
    source: Eleonore_von_Habsburg-Lothringen
    target: Ferdinand_Habsburg
  AddTriple (5f2ecd14-eb94-4f8c-89b9-39d3a0df6f8f)
 Call ID: 5f2ecd14-eb94-4f8c-89b9-39d3a0df6f8f
  Args:
    source: Ferdinand_Habsburg
    relation: :hasFather
    target: Karl_von_Habsburg
  AddTriple (8a36aac0-e32e-4ca0-80af-0f13ba135ffa)
 Call ID: 8a36aac0-e32e-4ca0-80af-0f13ba135ffa
  Args:
    relation: :hasMother
    source: Ferdinand_Habsburg
    target: Francesca_von_Thyssen-Bornemisza
  AssignClass (07fb174d-cadb-42f7-80e3-86a4e1deac65)
 Call ID: 07fb174d-cadb-42f7-80e3-86a4e1deac65
  Args:
    source: Jérôme_d'Ambrosio
    type: :Person
  AssignClass (f83d8230-de61-44fe-af15-6f622c8de825)
 Call ID: f83d8230-de61-44fe-af15-6f622c8de825
  Args:
    source: Jérôme_d'Ambrosio
    type: :Man
  AddLiteral (ab0cc72b-92c6-4305-bb14-7efd6324877e)
 Call ID: ab0cc72b-92c6-4305-bb14-7efd6324877e
  Args:
    relation: :hasMarriageYear
    source: Eleonore_von_Habsburg-Lothringen
    literal_value: 2020
    literal_type: xsd:integer
  AddTriple (5021131b-a9f8-466e-b91b-bdb1cd562095)
 Call ID: 5021131b-a9f8-466e-b91b-bdb1cd562095
  Args:
    source: Eleonore_von_Habsburg-Lothringen
    relation: :hasRelation
    target: Jérôme_d'Ambrosio
  AssignClass (9b827e10-b884-4f2a-8fb7-3476dad45329)
 Call ID: 9b827e10-b884-4f2a-8fb7-3476dad45329
  Args:
    source: Otto_d'Ambrosio
    type: :Person
  AssignClass (e4acf4e5-2309-4b86-9014-f1d960f82e91)
 Call ID: e4acf4e5-2309-4b86-9014-f1d960f82e91
  Args:
    source: Otto_d'Ambrosio
    type: :Man
  AddTriple (7610c5c0-654f-4803-b52b-7452fd7114e7)
 Call ID: 7610c5c0-654f-4803-b52b-7452fd7114e7
  Args:
    source: Eleonore_von_Habsburg-Lothringen
    relation: :hasSon
    target: Otto_d'Ambrosio
  AddTriple (f7a21ec0-55eb-4377-a602-f3611d903e85)
 Call ID: f7a21ec0-55eb-4377-a602-f3611d903e85
  Args:
    target: Jérôme_d'Ambrosio
    relation: :hasFather
    source: Otto_d'Ambrosio
  Finish (7ea17d58-6542-4d9c-ba8f-336b0bb98870)
 Call ID: 7ea17d58-6542-4d9c-ba8f-336b0bb98870
  Args: