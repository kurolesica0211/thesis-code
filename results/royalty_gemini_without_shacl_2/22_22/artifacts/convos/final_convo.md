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
  AssignClass (02d5afeb-d1bd-4e3e-879f-c9f709d15749)
 Call ID: 02d5afeb-d1bd-4e3e-879f-c9f709d15749
  Args:
    type: :Woman
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
  AssignClass (2bca49fb-f927-4a9b-8ea8-3e04518c69f3)
 Call ID: 2bca49fb-f927-4a9b-8ea8-3e04518c69f3
  Args:
    type: :Person
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
  AddLiteral (3162075b-0d07-462d-ad08-e40d6ef682a1)
 Call ID: 3162075b-0d07-462d-ad08-e40d6ef682a1
  Args:
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
    literal_type: xsd:string
    relation: :knownAs
    literal_value: Olympia
  AddLiteral (ec258252-bde2-4948-b2eb-fbd431b05b2d)
 Call ID: ec258252-bde2-4948-b2eb-fbd431b05b2d
  Args:
    relation: :hasBirthYear
    literal_value: 1996
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
    literal_type: xsd:integer
  AssignClass (6dcc6e6f-1518-489f-b252-ef4c0ab72dfa)
 Call ID: 6dcc6e6f-1518-489f-b252-ef4c0ab72dfa
  Args:
    type: :Man
    source: Pavlos_Crown_Prince_of_Greece
  AssignClass (6918decb-c7f5-4af5-a98c-c08982a194b6)
 Call ID: 6918decb-c7f5-4af5-a98c-c08982a194b6
  Args:
    type: :Person
    source: Pavlos_Crown_Prince_of_Greece
  AssignClass (c3a6c9bf-137e-4a17-b448-30464c3d8f45)
 Call ID: c3a6c9bf-137e-4a17-b448-30464c3d8f45
  Args:
    type: :Woman
    source: Marie-Chantal_Miller
  AssignClass (f9bee635-02ce-42ae-b152-e68418be54c8)
 Call ID: f9bee635-02ce-42ae-b152-e68418be54c8
  Args:
    type: :Person
    source: Marie-Chantal_Miller
  AddTriple (eff3d284-8c44-44a0-b205-346ebf47a05b)
 Call ID: eff3d284-8c44-44a0-b205-346ebf47a05b
  Args:
    relation: :hasFather
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
    target: Pavlos_Crown_Prince_of_Greece
  AddTriple (325ae7f5-05e0-428b-993a-3fcfd70391e9)
 Call ID: 325ae7f5-05e0-428b-993a-3fcfd70391e9
  Args:
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
    target: Marie-Chantal_Miller
    relation: :hasMother
  AssignClass (151b312c-3ca4-4467-b378-21fd2d06050e)
 Call ID: 151b312c-3ca4-4467-b378-21fd2d06050e
  Args:
    type: :Man
    source: Constantine_II_of_Greece
  AssignClass (a142457a-e233-48ad-8fef-ee9d4fd306b8)
 Call ID: a142457a-e233-48ad-8fef-ee9d4fd306b8
  Args:
    type: :Person
    source: Constantine_II_of_Greece
  AssignClass (6f8eca81-281b-469a-9c44-e82bf46e17bf)
 Call ID: 6f8eca81-281b-469a-9c44-e82bf46e17bf
  Args:
    type: :Woman
    source: Anne-Marie_of_Denmark
  AssignClass (ed8e7897-0d8c-4e60-842e-46ed67753e98)
 Call ID: ed8e7897-0d8c-4e60-842e-46ed67753e98
  Args:
    type: :Person
    source: Anne-Marie_of_Denmark
  AddTriple (2b11ec6e-ea2e-4321-9e05-c01139c5aabf)
 Call ID: 2b11ec6e-ea2e-4321-9e05-c01139c5aabf
  Args:
    source: Pavlos_Crown_Prince_of_Greece
    target: Constantine_II_of_Greece
    relation: :hasFather
  AddTriple (f62a8493-9fb1-4cef-b0f3-c3c308a0e769)
 Call ID: f62a8493-9fb1-4cef-b0f3-c3c308a0e769
  Args:
    source: Pavlos_Crown_Prince_of_Greece
    target: Anne-Marie_of_Denmark
    relation: :hasMother
  AssignClass (0052e831-37cb-4211-a3df-50cbc38c8610)
 Call ID: 0052e831-37cb-4211-a3df-50cbc38c8610
  Args:
    type: :Man
    source: Robert_Warren_Miller
  AssignClass (4fbce262-c241-44fd-8212-5b49471ce7e3)
 Call ID: 4fbce262-c241-44fd-8212-5b49471ce7e3
  Args:
    type: :Person
    source: Robert_Warren_Miller
  AddTriple (4280dd73-a20f-4a67-aacc-81e221740fb8)
 Call ID: 4280dd73-a20f-4a67-aacc-81e221740fb8
  Args:
    relation: :hasFather
    target: Robert_Warren_Miller
    source: Marie-Chantal_Miller
  AssignClass (1740c815-3738-4a41-87e3-9acdb44fbd6e)
 Call ID: 1740c815-3738-4a41-87e3-9acdb44fbd6e
  Args:
    type: :Man
    source: Prince_Constantine-Alexios
  AssignClass (0c318cce-5e0c-4e15-a35e-bd3a2853f224)
 Call ID: 0c318cce-5e0c-4e15-a35e-bd3a2853f224
  Args:
    type: :Person
    source: Prince_Constantine-Alexios
  AssignClass (0715c7f5-c34d-4d74-8fea-d809b9c7606a)
 Call ID: 0715c7f5-c34d-4d74-8fea-d809b9c7606a
  Args:
    type: :Man
    source: Prince_Achileas-Andreas
  AssignClass (5678a227-5571-45fb-af7f-d408177437c7)
 Call ID: 5678a227-5571-45fb-af7f-d408177437c7
  Args:
    type: :Person
    source: Prince_Achileas-Andreas
  AssignClass (e36c7cf5-937b-4259-862b-0d6a52714f66)
 Call ID: e36c7cf5-937b-4259-862b-0d6a52714f66
  Args:
    type: :Man
    source: Prince_Odysseas_Kimon
  AssignClass (89b90b98-7270-4fd4-b62f-788a2fb855a4)
 Call ID: 89b90b98-7270-4fd4-b62f-788a2fb855a4
  Args:
    type: :Person
    source: Prince_Odysseas_Kimon
  AssignClass (719f6aaa-f87f-45f2-9c72-a10821881e55)
 Call ID: 719f6aaa-f87f-45f2-9c72-a10821881e55
  Args:
    type: :Man
    source: Prince_Aristidis-Stavros
  AssignClass (e4c7cf16-7056-4362-be6e-802987d72c0c)
 Call ID: e4c7cf16-7056-4362-be6e-802987d72c0c
  Args:
    type: :Person
    source: Prince_Aristidis-Stavros
  AddTriple (e9d06086-e5dd-47d9-9871-7e9c92c84db4)
 Call ID: e9d06086-e5dd-47d9-9871-7e9c92c84db4
  Args:
    relation: :isSiblingOf
    target: Prince_Constantine-Alexios
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
  AddTriple (a4b32649-4b2a-4148-8c08-a29e56124042)
 Call ID: a4b32649-4b2a-4148-8c08-a29e56124042
  Args:
    target: Prince_Achileas-Andreas
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
    relation: :isSiblingOf
  AddTriple (2e111240-a402-4e34-a9cd-c108dd8a3f3c)
 Call ID: 2e111240-a402-4e34-a9cd-c108dd8a3f3c
  Args:
    target: Prince_Odysseas_Kimon
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
    relation: :isSiblingOf
  AddTriple (8aaa5ac6-1cf7-4895-a69b-cd686f1c455b)
 Call ID: 8aaa5ac6-1cf7-4895-a69b-cd686f1c455b
  Args:
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
    target: Prince_Aristidis-Stavros
    relation: :isSiblingOf
  AssignClass (2b637977-f31f-4b72-a0e3-8fe8a0bbf686)
 Call ID: 2b637977-f31f-4b72-a0e3-8fe8a0bbf686
  Args:
    type: :Woman
    source: Princess_Alexia_of_Greece_and_Denmark
  AssignClass (44d0a5a0-1535-4bab-a232-12b4bf553170)
 Call ID: 44d0a5a0-1535-4bab-a232-12b4bf553170
  Args:
    type: :Person
    source: Princess_Alexia_of_Greece_and_Denmark
  AssignClass (c81c3488-7c4f-4e23-9d3a-d66493b9f0a9)
 Call ID: c81c3488-7c4f-4e23-9d3a-d66493b9f0a9
  Args:
    type: :Woman
    source: Pia_Getty
  AssignClass (fca48d46-aeb6-4907-a887-0eb081e661e0)
 Call ID: fca48d46-aeb6-4907-a887-0eb081e661e0
  Args:
    type: :Person
    source: Pia_Getty
  AssignClass (dbc9a55d-b9cd-4bd0-93fc-5639bad71812)
 Call ID: dbc9a55d-b9cd-4bd0-93fc-5639bad71812
  Args:
    type: :Man
    source: Charles_III
  AssignClass (00325ad3-5b78-4ac1-8d0a-d169c205d3c5)
 Call ID: 00325ad3-5b78-4ac1-8d0a-d169c205d3c5
  Args:
    type: :Person
    source: Charles_III
  AssignClass (f9520549-e5e6-41e3-8140-577fb025663d)
 Call ID: f9520549-e5e6-41e3-8140-577fb025663d
  Args:
    type: :Man
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (ed6e04ee-14e7-40ba-98cc-8ba57a816b09)
 Call ID: ed6e04ee-14e7-40ba-98cc-8ba57a816b09
  Args:
    type: :Person
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (969814cc-6f93-440d-b526-b916a0ba9eca)
 Call ID: 969814cc-6f93-440d-b526-b916a0ba9eca
  Args:
    type: :Woman
    source: Queen_Sofia_of_Spain
  AssignClass (09184c55-c648-413c-951e-a4775902cc15)
 Call ID: 09184c55-c648-413c-951e-a4775902cc15
  Args:
    type: :Person
    source: Queen_Sofia_of_Spain
  AssignClass (79fd6582-3827-4ce4-a351-d450da6ae7d3)
 Call ID: 79fd6582-3827-4ce4-a351-d450da6ae7d3
  Args:
    type: :Woman
    source: Marina_consort_of_Prince_Michael
  AssignClass (ce6fdacb-3e67-4faf-b02b-6f9f007b2f56)
 Call ID: ce6fdacb-3e67-4faf-b02b-6f9f007b2f56
  Args:
    type: :Person
    source: Marina_consort_of_Prince_Michael
  AssignClass (0e4b97ba-d834-4105-961a-c6974a04e208)
 Call ID: 0e4b97ba-d834-4105-961a-c6974a04e208
  Args:
    type: :Woman
    source: Princess_Theodora_of_Greece_and_Denmark
  AssignClass (33b570ec-92c5-4a00-90e5-5a9475804944)
 Call ID: 33b570ec-92c5-4a00-90e5-5a9475804944
  Args:
    type: :Person
    source: Princess_Theodora_of_Greece_and_Denmark
  AssignClass (a406f189-6330-4b49-b662-92eaae6d48c8)
 Call ID: a406f189-6330-4b49-b662-92eaae6d48c8
  Args:
    type: :Man
    source: Matthew_Kumar
  AssignClass (5120c509-c9b4-4ef2-8a6a-393c421a3821)
 Call ID: 5120c509-c9b4-4ef2-8a6a-393c421a3821
  Args:
    type: :Person
    source: Matthew_Kumar
  Finish (e845130e-345d-4743-a33e-e3664ae11eba)
 Call ID: e845130e-345d-4743-a33e-e3664ae11eba
  Args: