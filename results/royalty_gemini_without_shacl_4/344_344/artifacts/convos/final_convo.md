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
  AssignClass (36749ac1-184e-4a67-b769-ca7f63f88b48)
 Call ID: 36749ac1-184e-4a67-b769-ca7f63f88b48
  Args:
    source: Françoise_dOrléans
    type: :Woman
  AddLiteral (2b6f1477-bee1-4c52-a95b-a1d06aad3e2b)
 Call ID: 2b6f1477-bee1-4c52-a95b-a1d06aad3e2b
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1902
    source: Françoise_dOrléans
  AddLiteral (db7bf877-006a-4526-a18d-4496c67c634f)
 Call ID: db7bf877-006a-4526-a18d-4496c67c634f
  Args:
    source: Françoise_dOrléans
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1953
  AssignClass (0a85e189-b53f-4287-99e7-bfa2e53288cf)
 Call ID: 0a85e189-b53f-4287-99e7-bfa2e53288cf
  Args:
    source: Jean_dOrléans
    type: :Man
  AssignClass (bcd7189e-5bec-4685-82fd-90de8f6cc875)
 Call ID: bcd7189e-5bec-4685-82fd-90de8f6cc875
  Args:
    source: Isabelle_of_Orléans
    type: :Woman
  AddTriple (53014693-917a-49ce-ae24-bc762217a74d)
 Call ID: 53014693-917a-49ce-ae24-bc762217a74d
  Args:
    source: Françoise_dOrléans
    relation: :hasFather
    target: Jean_dOrléans
  AddTriple (03a92a18-31e5-4efe-9fea-95de41b0b593)
 Call ID: 03a92a18-31e5-4efe-9fea-95de41b0b593
  Args:
    source: Françoise_dOrléans
    target: Isabelle_of_Orléans
    relation: :hasMother
  AssignClass (947bfd6e-26a6-47eb-9de2-48c19296aa57)
 Call ID: 947bfd6e-26a6-47eb-9de2-48c19296aa57
  Args:
    source: Henri_Count_of_Paris
    type: :Man
  AddTriple (1951d720-989b-4773-8c94-26cf857dbf25)
 Call ID: 1951d720-989b-4773-8c94-26cf857dbf25
  Args:
    relation: :hasBrother
    target: Henri_Count_of_Paris
    source: Françoise_dOrléans
  AssignClass (68896006-bdfc-42e2-824c-e279e8b0120d)
 Call ID: 68896006-bdfc-42e2-824c-e279e8b0120d
  Args:
    source: Christopher_of_Greece_and_Denmark
    type: :Man
  AddLiteral (5eda9dc9-a3e0-4f62-9a28-c9fe2dc34fef)
 Call ID: 5eda9dc9-a3e0-4f62-9a28-c9fe2dc34fef
  Args:
    source: Françoise_dOrléans
    literal_value: 1929
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (a954f6ba-aced-467c-9088-ce9d526f78f3)
 Call ID: a954f6ba-aced-467c-9088-ce9d526f78f3
  Args:
    source: Françoise_dOrléans
    relation: :hasRelation
    target: Christopher_of_Greece_and_Denmark
  AssignClass (f9e86b2a-6fe6-4fff-acd5-18c43f8f1c3f)
 Call ID: f9e86b2a-6fe6-4fff-acd5-18c43f8f1c3f
  Args:
    type: :Man
    source: George_I_of_Greece
  AssignClass (63c4b511-c6f2-43b4-bdc6-64d4c95c4574)
 Call ID: 63c4b511-c6f2-43b4-bdc6-64d4c95c4574
  Args:
    type: :Woman
    source: Olga_Constantinovna_of_Russia
  AddTriple (6fa074a0-32d1-4cfc-92c9-430afd514e00)
 Call ID: 6fa074a0-32d1-4cfc-92c9-430afd514e00
  Args:
    source: Christopher_of_Greece_and_Denmark
    target: George_I_of_Greece
    relation: :hasFather
  AddTriple (f97d8937-fca7-4813-a795-1db46caee5c0)
 Call ID: f97d8937-fca7-4813-a795-1db46caee5c0
  Args:
    target: Olga_Constantinovna_of_Russia
    relation: :hasMother
    source: Christopher_of_Greece_and_Denmark
  AssignClass (84f530cd-62d8-4ace-b07e-f7eae18039fa)
 Call ID: 84f530cd-62d8-4ace-b07e-f7eae18039fa
  Args:
    source: Christian_IX_of_Denmark
    type: :Man
  AddTriple (3e652b51-b8d6-4178-8374-a38dc8293c50)
 Call ID: 3e652b51-b8d6-4178-8374-a38dc8293c50
  Args:
    relation: :hasFather
    target: Christian_IX_of_Denmark
    source: George_I_of_Greece
  AssignClass (1801238d-aff9-4e5a-bbb1-497b0e9b0e99)
 Call ID: 1801238d-aff9-4e5a-bbb1-497b0e9b0e99
  Args:
    source: Michael_of_Greece_and_Denmark
    type: :Man
  AddTriple (7eded4d9-ad27-4d64-beab-e7fbf4626a76)
 Call ID: 7eded4d9-ad27-4d64-beab-e7fbf4626a76
  Args:
    relation: :hasFather
    target: Christopher_of_Greece_and_Denmark
    source: Michael_of_Greece_and_Denmark
  AddTriple (179b25e6-54ed-4919-81ff-5060e1a3cbf2)
 Call ID: 179b25e6-54ed-4919-81ff-5060e1a3cbf2
  Args:
    source: Michael_of_Greece_and_Denmark
    relation: :hasMother
    target: Françoise_dOrléans
  AssignClass (003fe87f-e480-45a6-abee-2f9d7123e28f)
 Call ID: 003fe87f-e480-45a6-abee-2f9d7123e28f
  Args:
    type: :Woman
    source: Marina_Karella
  AddTriple (90b667e2-7724-429b-909c-a01e585e8ef3)
 Call ID: 90b667e2-7724-429b-909c-a01e585e8ef3
  Args:
    source: Michael_of_Greece_and_Denmark
    target: Marina_Karella
    relation: :hasRelation
  AssignClass (36bd3b13-c950-4ac4-a5a2-01dc94e8bae7)
 Call ID: 36bd3b13-c950-4ac4-a5a2-01dc94e8bae7
  Args:
    source: Alexandra_of_Greece
    type: :Woman
  AssignClass (738b8c2a-70fb-4d22-a5f5-7d00cf5674e5)
 Call ID: 738b8c2a-70fb-4d22-a5f5-7d00cf5674e5
  Args:
    source: Olga_of_Greece
    type: :Woman
  AssignClass (538654f3-689b-4c90-a656-7bc63cef25c0)
 Call ID: 538654f3-689b-4c90-a656-7bc63cef25c0
  Args:
    type: :Man
    source: Aimone_of_Savoy-Aosta
  AddTriple (ca363d0c-0717-45ed-9eec-f1cd2e5a5d0c)
 Call ID: ca363d0c-0717-45ed-9eec-f1cd2e5a5d0c
  Args:
    relation: :hasRelation
    target: Aimone_of_Savoy-Aosta
    source: Olga_of_Greece
  AssignClass (b2031f00-ba66-4a6e-bf61-57a10a949188)
 Call ID: b2031f00-ba66-4a6e-bf61-57a10a949188
  Args:
    source: Isabella_Princess
    type: :Woman
  AssignClass (333ea2c4-b19e-4f96-bae3-fa4a9fb4ad4c)
 Call ID: 333ea2c4-b19e-4f96-bae3-fa4a9fb4ad4c
  Args:
    source: Pierre_Murat
    type: :Man
  AddTriple (8287f9aa-d4d5-4276-9e5e-f7681c2e2515)
 Call ID: 8287f9aa-d4d5-4276-9e5e-f7681c2e2515
  Args:
    relation: :hasRelation
    target: Pierre_Murat
    source: Isabella_Princess
  Finish (c7d9b264-09e1-45fd-ad21-8ae30d474fa5)
 Call ID: c7d9b264-09e1-45fd-ad21-8ae30d474fa5
  Args: