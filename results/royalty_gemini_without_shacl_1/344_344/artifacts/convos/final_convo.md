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
Princess Françoise d'Orléans (Françoise Isabelle Louise Marie; 25 December 1902 - 25 February 1953) was born an Orléans Princess of France and became a Princess of Greece and Denmark by marriage.
She was thus a member of the Greek royal family and a descendant of the "Citizen-King" Louis Philippe I.


Life

Françoise d'Orléans was born in Paris, the second daughter of Jean d'Orléans, duc de Guise (an Orléanist pretender to the throne of France under the name Jean III) and his wife, the French Princess Isabelle of Orléans.
Françoise's brother, Prince Henri, Count of Paris, succeeded their father as the Orleanist pretender, under the name Henri VI.
In Palermo on 11 February 1929, she married Prince Christopher of Greece and Denmark (1888–1940).
This was Christopher's second marriage - he was the youngest son of King George I of Greece (1845–1913) and his wife, Grand Duchess Olga Constantinovna of Russia (1851–1926).
Through his father, he was thus a grandson of King Christian IX of Denmark (1818–1906), nicknamed "the father-in-law of Europe" due to his six children all marrying into other royal families.
They had only one child, the writer Prince Michael of Greece and Denmark (1939–2024), whose marriage to the Greek artist Marina Karella (born 1940) did not conform to the laws of the royal house and thus deprived him of all right of succession to the Greek throne.
She is grandmother of Princess Alexandra of Greece, an artist, art collector, arts patron, and child life specialist.
Her other grand-daughter is Princess Olga of Greece, who married Prince Aimone of Savoy-Aosta, one of two claimants to be Head of the House of Savoy.
The civil war in Greece was preventing her from entering, and the British government refused to grant her asylum.
Françoise and her son Michael went to Paris, where they lived in the home of Princess Isabella and her second husband, Prince Pierre Murat.
Françoise did not want to see anyone in their residence and rarely left her rooms.
She is buried alongside her husband in Tatoi Royal Cemetery, Greece.



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
  AssignClass (a41e103b-2832-4869-b646-ad5baaa743a2)
 Call ID: a41e103b-2832-4869-b646-ad5baaa743a2
  Args:
    type: :Woman
    source: Françoise_d'Orléans
  AssignClass (86ac6bac-0d28-4258-9831-50418f25e712)
 Call ID: 86ac6bac-0d28-4258-9831-50418f25e712
  Args:
    source: Françoise_d'Orléans
    type: :Person
  AddLiteral (0f76afe8-d6a3-415c-ade8-0fd837d6e172)
 Call ID: 0f76afe8-d6a3-415c-ade8-0fd837d6e172
  Args:
    literal_type: xsd:integer
    literal_value: 1902
    relation: :hasBirthYear
    source: Françoise_d'Orléans
  AddLiteral (068c57ac-df82-402a-af53-566e6707e18f)
 Call ID: 068c57ac-df82-402a-af53-566e6707e18f
  Args:
    relation: :hasDeathYear
    literal_value: 1953
    literal_type: xsd:integer
    source: Françoise_d'Orléans
  AssignClass (c0aa47cf-dfbc-4b11-98c2-c7a135ee8d1b)
 Call ID: c0aa47cf-dfbc-4b11-98c2-c7a135ee8d1b
  Args:
    source: Jean_d'Orléans
    type: :Man
  AssignClass (658a6a36-f1a4-497b-9684-632dd32665ea)
 Call ID: 658a6a36-f1a4-497b-9684-632dd32665ea
  Args:
    type: :Person
    source: Jean_d'Orléans
  AssignClass (f37e785c-4371-4f42-a0d9-2d5c512403ea)
 Call ID: f37e785c-4371-4f42-a0d9-2d5c512403ea
  Args:
    type: :Woman
    source: Isabelle_of_Orléans
  AssignClass (945acf79-3b8c-4409-a703-f1661b5649c6)
 Call ID: 945acf79-3b8c-4409-a703-f1661b5649c6
  Args:
    type: :Person
    source: Isabelle_of_Orléans
  AddTriple (0f9dd843-c88c-4114-abe9-12afaa7544bb)
 Call ID: 0f9dd843-c88c-4114-abe9-12afaa7544bb
  Args:
    target: Jean_d'Orléans
    source: Françoise_d'Orléans
    relation: :hasFather
  AddTriple (cc9bb8fa-00dc-459c-80ac-1aa7c00041a0)
 Call ID: cc9bb8fa-00dc-459c-80ac-1aa7c00041a0
  Args:
    relation: :hasMother
    source: Françoise_d'Orléans
    target: Isabelle_of_Orléans
  AssignClass (16488414-9bf8-4976-8304-85183ac7fe7b)
 Call ID: 16488414-9bf8-4976-8304-85183ac7fe7b
  Args:
    source: Henri_Count_of_Paris
    type: :Man
  AssignClass (e19210ce-723c-4500-83da-bcb57f64fa21)
 Call ID: e19210ce-723c-4500-83da-bcb57f64fa21
  Args:
    source: Henri_Count_of_Paris
    type: :Person
  AddTriple (3b49cdfa-4815-4c0f-815d-8c8676bfca51)
 Call ID: 3b49cdfa-4815-4c0f-815d-8c8676bfca51
  Args:
    relation: :hasBrother
    source: Françoise_d'Orléans
    target: Henri_Count_of_Paris
  AssignClass (a6254f8a-844b-4bc0-a271-a3e721c26c59)
 Call ID: a6254f8a-844b-4bc0-a271-a3e721c26c59
  Args:
    type: :Man
    source: Christopher_of_Greece_and_Denmark
  AssignClass (d3273c2d-4351-495a-9c86-b14559662dc6)
 Call ID: d3273c2d-4351-495a-9c86-b14559662dc6
  Args:
    type: :Person
    source: Christopher_of_Greece_and_Denmark
  AddLiteral (03f6cc8b-058a-46f1-bd22-66c8359476a6)
 Call ID: 03f6cc8b-058a-46f1-bd22-66c8359476a6
  Args:
    relation: :hasMarriageYear
    literal_value: 1929
    literal_type: xsd:integer
    source: Françoise_d'Orléans
  AddTriple (5bcfa995-76eb-426d-8f69-cd5e762c956d)
 Call ID: 5bcfa995-76eb-426d-8f69-cd5e762c956d
  Args:
    source: Françoise_d'Orléans
    target: Christopher_of_Greece_and_Denmark
    relation: :hasRelation
  AddLiteral (6ce6049e-c04f-4bfb-a084-c36f3d992cec)
 Call ID: 6ce6049e-c04f-4bfb-a084-c36f3d992cec
  Args:
    relation: :hasBirthYear
    literal_value: 1888
    literal_type: xsd:integer
    source: Christopher_of_Greece_and_Denmark
  AddLiteral (e800d373-0f8e-4f32-9813-3d446bae80a1)
 Call ID: e800d373-0f8e-4f32-9813-3d446bae80a1
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1940
    source: Christopher_of_Greece_and_Denmark
  AssignClass (d9b70caa-4f07-440f-975b-1feca2bf7ddb)
 Call ID: d9b70caa-4f07-440f-975b-1feca2bf7ddb
  Args:
    type: :Man
    source: George_I_of_Greece
  AssignClass (9d9680a7-db70-4aaf-9f8e-779b51e4f919)
 Call ID: 9d9680a7-db70-4aaf-9f8e-779b51e4f919
  Args:
    type: :Person
    source: George_I_of_Greece
  AssignClass (39294c4f-9597-49e3-945c-3d0def38fb61)
 Call ID: 39294c4f-9597-49e3-945c-3d0def38fb61
  Args:
    source: Olga_Constantinovna_of_Russia
    type: :Woman
  AssignClass (9cac7f16-7a54-45af-8a1e-cef4fa53ab24)
 Call ID: 9cac7f16-7a54-45af-8a1e-cef4fa53ab24
  Args:
    source: Olga_Constantinovna_of_Russia
    type: :Person
  AddTriple (67b9f432-d46a-4bf4-adb2-b5dd84e081f9)
 Call ID: 67b9f432-d46a-4bf4-adb2-b5dd84e081f9
  Args:
    source: Christopher_of_Greece_and_Denmark
    target: George_I_of_Greece
    relation: :hasFather
  AddTriple (3be984d9-b819-4c2d-b5f0-4a2148a7371d)
 Call ID: 3be984d9-b819-4c2d-b5f0-4a2148a7371d
  Args:
    source: Christopher_of_Greece_and_Denmark
    target: Olga_Constantinovna_of_Russia
    relation: :hasMother
  AssignClass (62777d33-4a4d-4786-80f9-64805468dfa6)
 Call ID: 62777d33-4a4d-4786-80f9-64805468dfa6
  Args:
    type: :Man
    source: Christian_IX_of_Denmark
  AssignClass (574b8fef-b2c6-460f-8f5d-898033a8ad20)
 Call ID: 574b8fef-b2c6-460f-8f5d-898033a8ad20
  Args:
    source: Christian_IX_of_Denmark
    type: :Person
  AddTriple (d21fdeee-14f5-46f9-b6d7-d31c519eab34)
 Call ID: d21fdeee-14f5-46f9-b6d7-d31c519eab34
  Args:
    relation: :hasFather
    source: George_I_of_Greece
    target: Christian_IX_of_Denmark
  AssignClass (c3f53ad0-05f4-487b-be26-60ae96574b6a)
 Call ID: c3f53ad0-05f4-487b-be26-60ae96574b6a
  Args:
    source: Michael_of_Greece_and_Denmark
    type: :Man
  AssignClass (fd227199-554e-4db8-b6f6-0ae368f363f0)
 Call ID: fd227199-554e-4db8-b6f6-0ae368f363f0
  Args:
    source: Michael_of_Greece_and_Denmark
    type: :Person
  AddTriple (b74c27a9-4407-428e-8b2f-27e7575233cc)
 Call ID: b74c27a9-4407-428e-8b2f-27e7575233cc
  Args:
    relation: :hasChild
    target: Michael_of_Greece_and_Denmark
    source: Françoise_d'Orléans
  AddTriple (30030069-7dd7-47fe-a3c4-326ce56cb958)
 Call ID: 30030069-7dd7-47fe-a3c4-326ce56cb958
  Args:
    source: Christopher_of_Greece_and_Denmark
    target: Michael_of_Greece_and_Denmark
    relation: :hasChild
  AssignClass (dd4dc3bb-c319-4fda-ad2d-a161409a27fa)
 Call ID: dd4dc3bb-c319-4fda-ad2d-a161409a27fa
  Args:
    source: Marina_Karella
    type: :Woman
  AssignClass (ddf5e7a6-78c0-45c7-8370-76800dc029f4)
 Call ID: ddf5e7a6-78c0-45c7-8370-76800dc029f4
  Args:
    source: Marina_Karella
    type: :Person
  AddTriple (055cdba1-00ca-409c-b3ab-4b7f6eee5e64)
 Call ID: 055cdba1-00ca-409c-b3ab-4b7f6eee5e64
  Args:
    target: Marina_Karella
    source: Michael_of_Greece_and_Denmark
    relation: :hasRelation
  AssignClass (a9e52892-9b9d-4ea3-94e0-bf22713210e4)
 Call ID: a9e52892-9b9d-4ea3-94e0-bf22713210e4
  Args:
    type: :Woman
    source: Alexandra_of_Greece
  AssignClass (6b175afb-1ea4-4846-8259-521b336e42fe)
 Call ID: 6b175afb-1ea4-4846-8259-521b336e42fe
  Args:
    type: :Person
    source: Alexandra_of_Greece
  AssignClass (33788253-0a5f-427e-b871-d4193c254b68)
 Call ID: 33788253-0a5f-427e-b871-d4193c254b68
  Args:
    type: :Woman
    source: Olga_of_Greece
  AssignClass (ee13f4e3-aa29-42cf-be1c-96f8f79323f4)
 Call ID: ee13f4e3-aa29-42cf-be1c-96f8f79323f4
  Args:
    type: :Person
    source: Olga_of_Greece
  AssignClass (9a605987-7d9e-4624-8cc4-fc2a3a2b2709)
 Call ID: 9a605987-7d9e-4624-8cc4-fc2a3a2b2709
  Args:
    source: Aimone_of_Savoy-Aosta
    type: :Man
  AssignClass (428660aa-0a83-4605-81ba-99800a75c494)
 Call ID: 428660aa-0a83-4605-81ba-99800a75c494
  Args:
    source: Aimone_of_Savoy-Aosta
    type: :Person
  AddTriple (8d60b077-bb61-4aa9-a7ef-9035c175e6fa)
 Call ID: 8d60b077-bb61-4aa9-a7ef-9035c175e6fa
  Args:
    source: Olga_of_Greece
    target: Aimone_of_Savoy-Aosta
    relation: :hasRelation
  AssignClass (d9c854b8-8bfa-41ef-8c30-530a7d7c99d7)
 Call ID: d9c854b8-8bfa-41ef-8c30-530a7d7c99d7
  Args:
    source: Isabella_Princess
    type: :Woman
  AssignClass (b12b4f9e-c87f-47dd-9b87-24f0e6b80528)
 Call ID: b12b4f9e-c87f-47dd-9b87-24f0e6b80528
  Args:
    type: :Person
    source: Isabella_Princess
  AssignClass (5b1e9ecc-70a7-4792-bf8c-b17b078cf343)
 Call ID: 5b1e9ecc-70a7-4792-bf8c-b17b078cf343
  Args:
    source: Pierre_Murat
    type: :Man
  AssignClass (417e57dc-1baf-48e6-a022-b343c1896cdb)
 Call ID: 417e57dc-1baf-48e6-a022-b343c1896cdb
  Args:
    type: :Person
    source: Pierre_Murat
  AddTriple (4100e8cc-4606-4364-b543-bd76f539cf8b)
 Call ID: 4100e8cc-4606-4364-b543-bd76f539cf8b
  Args:
    target: Pierre_Murat
    source: Isabella_Princess
    relation: :hasRelation
  Finish (a3d68a1f-8616-436d-a7da-7f8ef1a04b7a)
 Call ID: a3d68a1f-8616-436d-a7da-7f8ef1a04b7a
  Args: