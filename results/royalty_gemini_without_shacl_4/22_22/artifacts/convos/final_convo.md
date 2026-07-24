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
Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


Princess Maria-Olympia of Greece and Denmark (Greek: Μαρία Ολυμπία Ντε Γκρες, romanized: María-Olympía de Grèce; born 25 July 1996) is a fashion model, socialite and member of the former Greek royal family.
She is the oldest child and only daughter of Pavlos, Crown Prince of Greece, and his wife, Marie-Chantal Miller.
Her paternal grandparents are Constantine II of Greece and Anne-Marie of Denmark, who were the last King and Queen of the Hellenes, while her maternal grandfather is duty free entrepreneur Robert Warren Miller.
Early life

Princess Maria-Olympia of Greece and Denmark was born on 25 July 1996 at Weill Cornell Medical Center in Lenox Hill, New York in Manhattan to Pavlos, Crown Prince of Greece, and his wife, Marie-Chantal.
Her godparents are her paternal aunt Princess Alexia of Greece and Denmark, her maternal aunt Pia Getty, her grandfather's second cousin Charles III, and Prince Michael of Greece and Denmark.
She is the older sister of Prince Constantine-Alexios, Prince Achileas-Andreas, Prince Odysseas Kimon, and Prince Aristidis-Stavros.
She uses the name Olympia in everyday life.
Olympia attended her first couture show around the age of 11 in Rome together with her parents.
Maria-Olympia registered at college in New York in the fall of 2015.
Fashion career

In April 2016, Maria-Olympia posed alongside two of her first cousins, Isabel Getty and Princess Talita
She has modeled for Teen Vogue, Town & Country, Tatler, Hello!, ¡Hola!, and W. In June 2017, Maria-Olympia walked the runway for Dolce & Gabbana.
Using her name Olympia the Saks Potts S/S 2019 show during Copenhagen Fashion Week in August 2018 was named OLYMPIA after her and opened by the princess herself as the first model on the stage.
Personal life

It was reported in May 2016 that Maria-Olympia was romantically involved with her godfather's son and third cousin once removed Prince Harry, but a representative of the British royal family denied the rumors.
On 28 September 2024, she served as a bridesmaid at the wedding of her aunt Princess Theodora of Greece and Denmark and Matthew Kumar at the Metropolitan Cathedral in Athens.
Οn 20 December 2024, Maria-Olympia acquired Greek citizenship, along with other members of the former Greek royal family, under the surname de Grèce.



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
  AssignClass (70a5f917-81e4-4c24-a7e6-244874479965)
 Call ID: 70a5f917-81e4-4c24-a7e6-244874479965
  Args:
    type: :Person
    source: Maria-Olympia of Greece and Denmark
  AssignClass (67c71e55-e707-4ac8-a904-0071b496b658)
 Call ID: 67c71e55-e707-4ac8-a904-0071b496b658
  Args:
    type: :Woman
    source: Maria-Olympia of Greece and Denmark
  AddLiteral (9157eed0-7e75-4866-91b4-e79c893130fd)
 Call ID: 9157eed0-7e75-4866-91b4-e79c893130fd
  Args:
    literal_type: xsd:positiveInteger
    source: Maria-Olympia of Greece and Denmark
    relation: :hasBirthYear
    literal_value: 1996
  AddLiteral (6ab68ec1-560b-460d-bc9b-aab89c979884)
 Call ID: 6ab68ec1-560b-460d-bc9b-aab89c979884
  Args:
    relation: :knownAs
    literal_value: Olympia
    literal_type: xsd:string
    source: Maria-Olympia of Greece and Denmark
  AssignClass (73f83192-d587-42e3-9286-90f10dcf7c4e)
 Call ID: 73f83192-d587-42e3-9286-90f10dcf7c4e
  Args:
    type: :Person
    source: Pavlos, Crown Prince of Greece
  AssignClass (921293eb-df8f-4e44-8465-51736a0106aa)
 Call ID: 921293eb-df8f-4e44-8465-51736a0106aa
  Args:
    source: Pavlos, Crown Prince of Greece
    type: :Man
  AssignClass (187e2cc9-4e73-4f0b-b98c-923d47faf6ae)
 Call ID: 187e2cc9-4e73-4f0b-b98c-923d47faf6ae
  Args:
    type: :Person
    source: Marie-Chantal Miller
  AssignClass (b0b112e5-ceee-467f-9951-893bfd098ff9)
 Call ID: b0b112e5-ceee-467f-9951-893bfd098ff9
  Args:
    type: :Woman
    source: Marie-Chantal Miller
  AddTriple (94e51e12-00bc-4bb5-b285-58dacdd92794)
 Call ID: 94e51e12-00bc-4bb5-b285-58dacdd92794
  Args:
    source: Pavlos, Crown Prince of Greece
    relation: :isFatherOf
    target: Maria-Olympia of Greece and Denmark
  AddTriple (b455e4ff-49fb-41fc-9029-e1c131df03b1)
 Call ID: b455e4ff-49fb-41fc-9029-e1c131df03b1
  Args:
    source: Marie-Chantal Miller
    target: Maria-Olympia of Greece and Denmark
    relation: :isMotherOf
  AssignClass (41f6e404-a9c4-4e90-b7bc-2d973ba91aa1)
 Call ID: 41f6e404-a9c4-4e90-b7bc-2d973ba91aa1
  Args:
    type: :Person
    source: Constantine II of Greece
  AssignClass (271e73ae-453e-484d-a523-a04bccd44832)
 Call ID: 271e73ae-453e-484d-a523-a04bccd44832
  Args:
    type: :Man
    source: Constantine II of Greece
  AssignClass (8f5d60c8-de59-4fbd-94d8-d4b760adbf7f)
 Call ID: 8f5d60c8-de59-4fbd-94d8-d4b760adbf7f
  Args:
    source: Anne-Marie of Denmark
    type: :Person
  AssignClass (6c6f4f48-27f1-466c-aadd-c0481a73bb46)
 Call ID: 6c6f4f48-27f1-466c-aadd-c0481a73bb46
  Args:
    source: Anne-Marie of Denmark
    type: :Woman
  AddTriple (9140d0dc-a57a-4221-b224-1d1087be2389)
 Call ID: 9140d0dc-a57a-4221-b224-1d1087be2389
  Args:
    relation: :isFatherOf
    target: Pavlos, Crown Prince of Greece
    source: Constantine II of Greece
  AddTriple (1ad2ddea-a951-4ead-b560-dbfb044f70e4)
 Call ID: 1ad2ddea-a951-4ead-b560-dbfb044f70e4
  Args:
    relation: :isMotherOf
    target: Pavlos, Crown Prince of Greece
    source: Anne-Marie of Denmark
  AssignClass (2c77c626-5da6-439c-ae01-3e12d7e1f988)
 Call ID: 2c77c626-5da6-439c-ae01-3e12d7e1f988
  Args:
    source: Robert Warren Miller
    type: :Person
  AssignClass (8495a899-0670-49b8-b5a4-9f6a2c8e1bd6)
 Call ID: 8495a899-0670-49b8-b5a4-9f6a2c8e1bd6
  Args:
    source: Robert Warren Miller
    type: :Man
  AddTriple (7cb40fc6-1645-4dad-9ff6-2453f87af983)
 Call ID: 7cb40fc6-1645-4dad-9ff6-2453f87af983
  Args:
    target: Marie-Chantal Miller
    relation: :isFatherOf
    source: Robert Warren Miller
  AssignClass (07bd7a10-525e-43d3-aed8-ff9eb8893faf)
 Call ID: 07bd7a10-525e-43d3-aed8-ff9eb8893faf
  Args:
    type: :Person
    source: Prince Constantine-Alexios
  AssignClass (31db8aeb-d32a-49ed-b961-3516fe03c81d)
 Call ID: 31db8aeb-d32a-49ed-b961-3516fe03c81d
  Args:
    type: :Man
    source: Prince Constantine-Alexios
  AssignClass (358e9896-d29a-4aae-b083-9d00b85744e3)
 Call ID: 358e9896-d29a-4aae-b083-9d00b85744e3
  Args:
    type: :Person
    source: Prince Achileas-Andreas
  AssignClass (03004b31-f931-41c7-821c-2a2add2205ef)
 Call ID: 03004b31-f931-41c7-821c-2a2add2205ef
  Args:
    type: :Man
    source: Prince Achileas-Andreas
  AssignClass (2327039b-4ace-4010-b254-c578feba2941)
 Call ID: 2327039b-4ace-4010-b254-c578feba2941
  Args:
    source: Prince Odysseas Kimon
    type: :Person
  AssignClass (478c740d-fe71-4172-8d7e-1590bacbd804)
 Call ID: 478c740d-fe71-4172-8d7e-1590bacbd804
  Args:
    source: Prince Odysseas Kimon
    type: :Man
  AssignClass (39f8f228-9857-4f8e-962e-de25b764b19f)
 Call ID: 39f8f228-9857-4f8e-962e-de25b764b19f
  Args:
    source: Prince Aristidis-Stavros
    type: :Person
  AssignClass (f78d6a8f-8ac0-4a6a-b8b2-57a1f6502b9f)
 Call ID: f78d6a8f-8ac0-4a6a-b8b2-57a1f6502b9f
  Args:
    type: :Man
    source: Prince Aristidis-Stavros
  AddTriple (e1eaff73-9e12-43e6-84cd-9ffca1cacada)
 Call ID: e1eaff73-9e12-43e6-84cd-9ffca1cacada
  Args:
    target: Prince Constantine-Alexios
    relation: :isSiblingOf
    source: Maria-Olympia of Greece and Denmark
  AddTriple (98562453-b2e5-4289-990e-87c97f63de9e)
 Call ID: 98562453-b2e5-4289-990e-87c97f63de9e
  Args:
    source: Maria-Olympia of Greece and Denmark
    target: Prince Achileas-Andreas
    relation: :isSiblingOf
  AddTriple (e79114c1-a63f-49d4-a4c0-28a8da157de1)
 Call ID: e79114c1-a63f-49d4-a4c0-28a8da157de1
  Args:
    source: Maria-Olympia of Greece and Denmark
    relation: :isSiblingOf
    target: Prince Odysseas Kimon
  AddTriple (2c7bfcbd-512b-4f2e-9683-8d582a9016cb)
 Call ID: 2c7bfcbd-512b-4f2e-9683-8d582a9016cb
  Args:
    source: Maria-Olympia of Greece and Denmark
    relation: :isSiblingOf
    target: Prince Aristidis-Stavros
  AssignClass (4578d5b8-1b99-486e-bc07-2d273db3f682)
 Call ID: 4578d5b8-1b99-486e-bc07-2d273db3f682
  Args:
    type: :Person
    source: Princess Alexia of Greece and Denmark
  AssignClass (0908983a-1543-4864-90e1-80afeed4d486)
 Call ID: 0908983a-1543-4864-90e1-80afeed4d486
  Args:
    source: Princess Alexia of Greece and Denmark
    type: :Woman
  AssignClass (43866925-3326-4dd8-9a4d-8a5ac4637011)
 Call ID: 43866925-3326-4dd8-9a4d-8a5ac4637011
  Args:
    source: Pia Getty
    type: :Person
  AssignClass (9ee15361-d7e5-43a9-8003-4d7d39f636eb)
 Call ID: 9ee15361-d7e5-43a9-8003-4d7d39f636eb
  Args:
    type: :Woman
    source: Pia Getty
  AssignClass (c9c96890-fca1-44ba-bc58-c0b4cf476bbc)
 Call ID: c9c96890-fca1-44ba-bc58-c0b4cf476bbc
  Args:
    source: Charles III
    type: :Person
  AssignClass (79b5df7d-8e7a-4f0a-8b51-422c93dfed0e)
 Call ID: 79b5df7d-8e7a-4f0a-8b51-422c93dfed0e
  Args:
    type: :Man
    source: Charles III
  AssignClass (b6166429-6921-4b2f-ac1b-a39e923526ef)
 Call ID: b6166429-6921-4b2f-ac1b-a39e923526ef
  Args:
    type: :Person
    source: Prince Michael of Greece and Denmark
  AssignClass (9c062ccf-be71-4bd7-927b-39caeac0e586)
 Call ID: 9c062ccf-be71-4bd7-927b-39caeac0e586
  Args:
    type: :Man
    source: Prince Michael of Greece and Denmark
  AssignClass (7cf8d209-d52b-499d-bea8-5c76aa9e8fd7)
 Call ID: 7cf8d209-d52b-499d-bea8-5c76aa9e8fd7
  Args:
    source: Princess Theodora of Greece and Denmark
    type: :Person
  AssignClass (01576ab2-b65b-42f3-a9e8-f75c1e0a158d)
 Call ID: 01576ab2-b65b-42f3-a9e8-f75c1e0a158d
  Args:
    type: :Woman
    source: Princess Theodora of Greece and Denmark
  AssignClass (0349c066-d8fd-4cc0-8e25-3d4ed82f6c14)
 Call ID: 0349c066-d8fd-4cc0-8e25-3d4ed82f6c14
  Args:
    type: :Person
    source: Matthew Kumar
  AssignClass (58136722-73c0-4d25-94f1-b717d1e3c84b)
 Call ID: 58136722-73c0-4d25-94f1-b717d1e3c84b
  Args:
    source: Matthew Kumar
    type: :Man
  AssignClass (11f15b5f-12d9-4bd0-be7e-78e7b0ea4c03)
 Call ID: 11f15b5f-12d9-4bd0-be7e-78e7b0ea4c03
  Args:
    type: :Person
    source: Queen Sofía of Spain
  AssignClass (0aaace61-9b77-4fc3-b4c4-8f3a1ee144aa)
 Call ID: 0aaace61-9b77-4fc3-b4c4-8f3a1ee144aa
  Args:
    source: Queen Sofía of Spain
    type: :Woman
  AssignClass (831e0a14-1c45-4ee3-bd59-8a260893636f)
 Call ID: 831e0a14-1c45-4ee3-bd59-8a260893636f
  Args:
    source: Marina, consort of Prince Michael
    type: :Person
  AssignClass (1451daa3-b0ed-42a8-83da-835c28546b5e)
 Call ID: 1451daa3-b0ed-42a8-83da-835c28546b5e
  Args:
    type: :Woman
    source: Marina, consort of Prince Michael
  Finish (8cc26c23-c808-471f-9654-21a34f495f07)
 Call ID: 8cc26c23-c808-471f-9654-21a34f495f07
  Args: