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
Alexander Mountstuart Elphinstone, 19th Lord Elphinstone, 5th Baron Elphinstone (born 15 April 1980), is a Scottish peer in both the Peerage of Scotland and the Peerage of the United Kingdom.
Early life and family

Lord Elphinstone is the son of James Elphinstone, 18th Lord Elphinstone, and Willa Mary Gabrielle Chetwode.
His mother is the daughter of Major George Chetwode and Lady Willa Elliot-Murray-Kynynmound, daughter of Victor Elliot-Murray-Kynynmound, 5th Earl of Minto.
Lord Elphinstone's paternal grandfather, Rev. Hon.
Andrew Elphinstone, was a first cousin of Elizabeth II through his mother, the former Lady Mary Bowes-Lyon, who was an elder sister of Queen Elizabeth The Queen Mother.
Notes

References




This biography of a Lord of Parliament in the Peerage of Scotland is a stub.



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
  AssignClass (1a5a2733-72d2-4e0c-9d8f-8fb763d18aea)
 Call ID: 1a5a2733-72d2-4e0c-9d8f-8fb763d18aea
  Args:
    type: :Man
    source: Alexander_Mountstuart_Elphinstone
  AssignClass (0c06353c-0849-4577-9332-b5a9fcf7305a)
 Call ID: 0c06353c-0849-4577-9332-b5a9fcf7305a
  Args:
    type: :Person
    source: Alexander_Mountstuart_Elphinstone
  AddLiteral (97af29f0-0128-490f-9fdf-d9edc8f7a129)
 Call ID: 97af29f0-0128-490f-9fdf-d9edc8f7a129
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Alexander_Mountstuart_Elphinstone
    literal_value: 1980
  AssignClass (7eadca38-3d50-4392-a345-728e957811ed)
 Call ID: 7eadca38-3d50-4392-a345-728e957811ed
  Args:
    type: :Man
    source: James_Elphinstone
  AssignClass (6e163414-5f22-4266-8fee-58d6cbdb5648)
 Call ID: 6e163414-5f22-4266-8fee-58d6cbdb5648
  Args:
    type: :Person
    source: James_Elphinstone
  AddTriple (aa6092c5-d334-41db-bf90-f70ca149a87e)
 Call ID: aa6092c5-d334-41db-bf90-f70ca149a87e
  Args:
    target: James_Elphinstone
    relation: :hasFather
    source: Alexander_Mountstuart_Elphinstone
  AssignClass (e38be0cf-033d-49ee-954b-541fd05c0f8d)
 Call ID: e38be0cf-033d-49ee-954b-541fd05c0f8d
  Args:
    type: :Woman
    source: Willa_Mary_Gabrielle_Chetwode
  AssignClass (25730645-9f33-4880-a4b4-35827f9afeff)
 Call ID: 25730645-9f33-4880-a4b4-35827f9afeff
  Args:
    type: :Person
    source: Willa_Mary_Gabrielle_Chetwode
  AddTriple (e3e5cb6d-5c83-46e7-8c0a-f0d621e8f06b)
 Call ID: e3e5cb6d-5c83-46e7-8c0a-f0d621e8f06b
  Args:
    relation: :hasMother
    source: Alexander_Mountstuart_Elphinstone
    target: Willa_Mary_Gabrielle_Chetwode
  AssignClass (025eb624-2054-483b-b932-7a63f7a540fc)
 Call ID: 025eb624-2054-483b-b932-7a63f7a540fc
  Args:
    type: :Man
    source: Major_George_Chetwode
  AssignClass (d4a0ef03-c5ce-4ef5-b8c8-071362e93775)
 Call ID: d4a0ef03-c5ce-4ef5-b8c8-071362e93775
  Args:
    type: :Person
    source: Major_George_Chetwode
  AddTriple (06197fd4-3551-46bf-af37-311827d0c185)
 Call ID: 06197fd4-3551-46bf-af37-311827d0c185
  Args:
    target: Major_George_Chetwode
    source: Willa_Mary_Gabrielle_Chetwode
    relation: :hasFather
  AssignClass (c0a25b2a-a95e-4b9d-962d-bef211c29e6b)
 Call ID: c0a25b2a-a95e-4b9d-962d-bef211c29e6b
  Args:
    type: :Woman
    source: Lady_Willa_Elliot-Murray-Kynynmound
  AssignClass (9f544838-b58a-4161-b309-c538eb9d586d)
 Call ID: 9f544838-b58a-4161-b309-c538eb9d586d
  Args:
    type: :Person
    source: Lady_Willa_Elliot-Murray-Kynynmound
  AddTriple (6c2a56f1-5a2f-4954-a603-beb23e07fb63)
 Call ID: 6c2a56f1-5a2f-4954-a603-beb23e07fb63
  Args:
    target: Lady_Willa_Elliot-Murray-Kynynmound
    source: Willa_Mary_Gabrielle_Chetwode
    relation: :hasMother
  AssignClass (1ad9da73-05a1-4a4e-a352-bc50c72443c5)
 Call ID: 1ad9da73-05a1-4a4e-a352-bc50c72443c5
  Args:
    type: :Man
    source: Victor_Elliot-Murray-Kynynmound
  AssignClass (15edcab2-9363-446c-aba8-9567e20aa9e5)
 Call ID: 15edcab2-9363-446c-aba8-9567e20aa9e5
  Args:
    type: :Person
    source: Victor_Elliot-Murray-Kynynmound
  AddTriple (3647f110-368f-40ff-bad5-e15e878ee5e2)
 Call ID: 3647f110-368f-40ff-bad5-e15e878ee5e2
  Args:
    target: Victor_Elliot-Murray-Kynynmound
    source: Lady_Willa_Elliot-Murray-Kynynmound
    relation: :hasFather
  AssignClass (570ba15b-45e2-4331-9ebd-b0181a63bc33)
 Call ID: 570ba15b-45e2-4331-9ebd-b0181a63bc33
  Args:
    type: :Man
    source: Rev_Hon_Andrew_Elphinstone
  AssignClass (8477a190-ee39-41bf-b556-8d73c0b78e45)
 Call ID: 8477a190-ee39-41bf-b556-8d73c0b78e45
  Args:
    type: :Person
    source: Rev_Hon_Andrew_Elphinstone
  AddTriple (fe426fa9-6ad5-402e-b90f-1766131975fa)
 Call ID: fe426fa9-6ad5-402e-b90f-1766131975fa
  Args:
    target: Rev_Hon_Andrew_Elphinstone
    source: James_Elphinstone
    relation: :hasFather
  AssignClass (f440bb91-d6dc-41f9-b329-2454fead1685)
 Call ID: f440bb91-d6dc-41f9-b329-2454fead1685
  Args:
    type: :Woman
    source: Lady_Mary_Bowes-Lyon
  AssignClass (2fec0403-a881-4bd9-833b-7d6616da6e01)
 Call ID: 2fec0403-a881-4bd9-833b-7d6616da6e01
  Args:
    type: :Person
    source: Lady_Mary_Bowes-Lyon
  AddTriple (bce70aa3-9234-47f7-8edf-295430991633)
 Call ID: bce70aa3-9234-47f7-8edf-295430991633
  Args:
    source: Rev_Hon_Andrew_Elphinstone
    relation: :hasMother
    target: Lady_Mary_Bowes-Lyon
  AssignClass (0de036d8-7e64-4110-83c6-6aefeadbb468)
 Call ID: 0de036d8-7e64-4110-83c6-6aefeadbb468
  Args:
    type: :Woman
    source: Elizabeth_II
  AssignClass (899d2801-4f25-41c6-a7d1-43ca4e57373c)
 Call ID: 899d2801-4f25-41c6-a7d1-43ca4e57373c
  Args:
    type: :Person
    source: Elizabeth_II
  AssignClass (c4103b93-baa8-4853-9183-f756d99001a7)
 Call ID: c4103b93-baa8-4853-9183-f756d99001a7
  Args:
    type: :Woman
    source: Queen_Elizabeth_The_Queen_Mother
  AssignClass (090f9fd6-be2a-4502-a3e5-1160e647e040)
 Call ID: 090f9fd6-be2a-4502-a3e5-1160e647e040
  Args:
    type: :Person
    source: Queen_Elizabeth_The_Queen_Mother
  AddTriple (8a483f5e-3066-4727-a96d-f1caa717041a)
 Call ID: 8a483f5e-3066-4727-a96d-f1caa717041a
  Args:
    source: Lady_Mary_Bowes-Lyon
    relation: :isSisterOf
    target: Queen_Elizabeth_The_Queen_Mother
  Finish (b4f5030c-c4b4-4769-9875-75fc61989e49)
 Call ID: b4f5030c-c4b4-4769-9875-75fc61989e49
  Args: