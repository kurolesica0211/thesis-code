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
Franz Wilhelm Victor Christoph Stephan Prinz von Preussen (born 3 September 1943) is a German businessman and member of the House of Hohenzollern, the former ruling German imperial house and royal house of Prussia.
He is also the great-grandson of German Emperor Wilhelm II.
Biography

Franz Wilhelm Prince of Prussia was born in Grünberg, Silesia, as the son of Prince Karl Franz of Prussia and his first wife Princess Henriette von Schönaich-Carolath.
He had a twin brother, Prince Friedrich Christian, who died three weeks after his birth.
Prince Franz Wilhelm is a grandson of Prince Joachim of Prussia, the youngest son of Emperor Wilhelm II.
In 2002 Franz Wilhelm with Theodor Tantzen founded the Prinz von Preußen Grundbesitz AG, a project development and project management company which restores old buildings in Germany.
Personal life

Franz Wilhelm married his third cousin once removed, Grand Duchess Maria Vladimirovna of Russia, great-great-granddaughter of Queen Victoria, civilly on 4 September 1976 at Dinard and religiously on 22 September at the Russian Orthodox Chapel in Madrid.
Before his marriage, he converted to the Russian Orthodox faith and was created a Grand Duke of Russia with the name Mikhail Pavlovich by his father-in-law Grand Duke Vladimir of Russia.
Franz Wilhelm and Grand Duchess Maria had one son before divorcing on 19 June 1985 (they separated in 1982), at which point he reverted to his previous title.
He married Nadia Nour El Etreby (born 2 August 1949) on 14 March 2019, to whom was bestowed upon marriage the courtesy style and title of Her Royal Highness Princess Franz Wilhelm of Prussia.



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
  AssignClass (6bac008b-ac06-4a8f-be99-0d0aae8769aa)
 Call ID: 6bac008b-ac06-4a8f-be99-0d0aae8769aa
  Args:
    source: Franz_Wilhelm_von_Preussen
    type: :Man
  AssignClass (2cae6e3e-cd3c-4074-acf8-b7a89911f006)
 Call ID: 2cae6e3e-cd3c-4074-acf8-b7a89911f006
  Args:
    source: Franz_Wilhelm_von_Preussen
    type: :Person
  AssignClass (234dfc15-fe34-41fb-9062-544ad2124e83)
 Call ID: 234dfc15-fe34-41fb-9062-544ad2124e83
  Args:
    source: Karl_Franz_of_Prussia
    type: :Man
  AssignClass (2e3cbd01-c30b-419a-b0d3-91fe0dfd56d6)
 Call ID: 2e3cbd01-c30b-419a-b0d3-91fe0dfd56d6
  Args:
    type: :Person
    source: Karl_Franz_of_Prussia
  AssignClass (54678070-67d7-4134-b543-3c2c11997308)
 Call ID: 54678070-67d7-4134-b543-3c2c11997308
  Args:
    source: Henriette_von_Schönaich-Carolath
    type: :Woman
  AssignClass (f22d7657-ddfc-45db-aead-7c9d34ee5722)
 Call ID: f22d7657-ddfc-45db-aead-7c9d34ee5722
  Args:
    type: :Person
    source: Henriette_von_Schönaich-Carolath
  AssignClass (2fc78caf-064c-4ab7-93e2-bfa2ad53ff49)
 Call ID: 2fc78caf-064c-4ab7-93e2-bfa2ad53ff49
  Args:
    source: Friedrich_Christian_of_Prussia
    type: :Man
  AssignClass (0223b1d8-c143-49eb-ac8a-c899397ad273)
 Call ID: 0223b1d8-c143-49eb-ac8a-c899397ad273
  Args:
    source: Friedrich_Christian_of_Prussia
    type: :Person
  AssignClass (16494d3e-4e93-464a-aff2-5d6219cdaeed)
 Call ID: 16494d3e-4e93-464a-aff2-5d6219cdaeed
  Args:
    type: :Man
    source: Joachim_of_Prussia
  AssignClass (56d8c2bf-6521-4ddf-ac01-231f6ef50d30)
 Call ID: 56d8c2bf-6521-4ddf-ac01-231f6ef50d30
  Args:
    type: :Person
    source: Joachim_of_Prussia
  AssignClass (14a8aa74-8cb4-4efc-9bca-d23bbb6be46d)
 Call ID: 14a8aa74-8cb4-4efc-9bca-d23bbb6be46d
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (2040b23e-2c61-40b4-a0aa-91ce70d79f64)
 Call ID: 2040b23e-2c61-40b4-a0aa-91ce70d79f64
  Args:
    source: Wilhelm_II
    type: :Person
  AssignClass (7dc3a034-4bb7-4def-8196-70f95c975ade)
 Call ID: 7dc3a034-4bb7-4def-8196-70f95c975ade
  Args:
    type: :Woman
    source: Maria_Vladimirovna_of_Russia
  AssignClass (b839ee0b-19cf-4d1c-8173-c74f17c4f138)
 Call ID: b839ee0b-19cf-4d1c-8173-c74f17c4f138
  Args:
    type: :Person
    source: Maria_Vladimirovna_of_Russia
  AssignClass (12beee91-42cc-43ef-9a48-2913a1c71f2f)
 Call ID: 12beee91-42cc-43ef-9a48-2913a1c71f2f
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (477a7953-e342-4348-96dd-680d060926f5)
 Call ID: 477a7953-e342-4348-96dd-680d060926f5
  Args:
    source: Queen_Victoria
    type: :Person
  AssignClass (98299237-fe94-47bd-953a-a37fdeba1f7a)
 Call ID: 98299237-fe94-47bd-953a-a37fdeba1f7a
  Args:
    source: Vladimir_of_Russia
    type: :Man
  AssignClass (4f205044-d979-4836-916a-df2c9060262f)
 Call ID: 4f205044-d979-4836-916a-df2c9060262f
  Args:
    source: Vladimir_of_Russia
    type: :Person
  AssignClass (97b2ac9b-3834-4c74-ac35-dca772ff9baf)
 Call ID: 97b2ac9b-3834-4c74-ac35-dca772ff9baf
  Args:
    source: Nadia_Nour_El_Etreby
    type: :Woman
  AssignClass (9c61dd7c-4f4f-4705-8744-ddbd724f8ed5)
 Call ID: 9c61dd7c-4f4f-4705-8744-ddbd724f8ed5
  Args:
    type: :Person
    source: Nadia_Nour_El_Etreby
  AddLiteral (7b071664-47c8-4f1d-bf06-77d21d61e3d7)
 Call ID: 7b071664-47c8-4f1d-bf06-77d21d61e3d7
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1943
    source: Franz_Wilhelm_von_Preussen
  AddTriple (85e8d701-736b-426e-9d72-4f27f8f7222a)
 Call ID: 85e8d701-736b-426e-9d72-4f27f8f7222a
  Args:
    target: Karl_Franz_of_Prussia
    source: Franz_Wilhelm_von_Preussen
    relation: :hasFather
  AddTriple (92ae33a1-13ed-4c4a-9043-2aae1af7ae17)
 Call ID: 92ae33a1-13ed-4c4a-9043-2aae1af7ae17
  Args:
    target: Henriette_von_Schönaich-Carolath
    source: Franz_Wilhelm_von_Preussen
    relation: :hasMother
  AddTriple (0121ad04-08b1-4258-b496-5077ac70aa92)
 Call ID: 0121ad04-08b1-4258-b496-5077ac70aa92
  Args:
    target: Friedrich_Christian_of_Prussia
    source: Franz_Wilhelm_von_Preussen
    relation: :hasBrother
  AddTriple (45509764-0588-437d-990b-5f3e1c9cb502)
 Call ID: 45509764-0588-437d-990b-5f3e1c9cb502
  Args:
    target: Joachim_of_Prussia
    source: Franz_Wilhelm_von_Preussen
    relation: :hasFather
  AddTriple (68967570-4226-4801-ab30-efa6f234d6b9)
 Call ID: 68967570-4226-4801-ab30-efa6f234d6b9
  Args:
    source: Joachim_of_Prussia
    relation: :hasFather
    target: Wilhelm_II
  AddTriple (66e5f80e-5d6c-44bc-bcf2-709af6a70f53)
 Call ID: 66e5f80e-5d6c-44bc-bcf2-709af6a70f53
  Args:
    relation: :hasFather
    source: Vladimir_of_Russia
    target: Maria_Vladimirovna_of_Russia
  AddLiteral (216d5c19-0d57-47f3-bd21-2345da9df4e5)
 Call ID: 216d5c19-0d57-47f3-bd21-2345da9df4e5
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1949
    source: Nadia_Nour_El_Etreby
  Finish (d3e712e4-5616-498d-adb2-30f9264b9345)
 Call ID: d3e712e4-5616-498d-adb2-30f9264b9345
  Args: