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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Constantijn of the Netherlands (Constantijn Christof Frederik Aschwin; born 11 October 1969) is the third and youngest son of the former Dutch queen, Beatrix, and her husband, Claus von Amsberg, and is the younger brother of the reigning Dutch king, Willem-Alexander.
Life and career

Prince Constantijn was born on 11 October 1969 at  Academic Hospital Utrecht (now the University Medical Center Utrecht) in Utrecht following the births of his brothers, Willem-Alexander (b. 1967), and Johan Friso (1968–2013).
His godparents are former King Constantine II of Greece (1940–2023), Prince Aschwin of Lippe-Biesterfeld, Axel Freiherr von dem Bussche-Streithorst, Max Kohnstamm, and Corinne de Beaufort-Sickinghe.
Prince Constantijn studied law at Leiden University, becoming a lawyer, and then worked at the Brussels department of the (Dutch) European Union commissioner of foreign relations, Hans van den Broek.
Furthermore, he has a part-time position at the Netherlands Ministry of Foreign Affairs in The Hague.
Prince Constantijn rarely attends public events in his capacity as a member of the Dutch royal family.
Marriage and family

The engagement of Prince Constantijn and Petra Laurentien Brinkhorst was announced on 16 December 2000.
Prince Constantijn and Princess Laurentien have three children: Eloise (b. 2002), Claus-Casimir (b. 2004), and Leonore (b. 2006).
Upon the abdication of Queen Beatrix on 30 April 2013, the children of Prince Constantijn and Princess Laurentien ceased to be members of the Royal House, although they continue to be members of the royal family and remain in the line of succession.
Honours and arms

National

Foreign

Arms

Ancestry

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (ca9854cc-4335-4691-8c4f-930c1b5f0709)
 Call ID: ca9854cc-4335-4691-8c4f-930c1b5f0709
  Args:
    source: Beatrix
    type: :Woman
  AssignClass (4fb56707-3905-4099-a0dc-22ca6f6db5f2)
 Call ID: 4fb56707-3905-4099-a0dc-22ca6f6db5f2
  Args:
    source: Margriet
    type: :Woman
  AssignClass (59596471-185a-48f8-b429-8afd0b0c2d6b)
 Call ID: 59596471-185a-48f8-b429-8afd0b0c2d6b
  Args:
    source: Pieter_van_Vollenhoven
    type: :Man
  AssignClass (1e0a7b57-7198-47a4-a135-40af3c1553db)
 Call ID: 1e0a7b57-7198-47a4-a135-40af3c1553db
  Args:
    source: Constantijn
    type: :Man
  AssignClass (d51b4d22-8acc-4578-ab1e-2a557df42bf4)
 Call ID: d51b4d22-8acc-4578-ab1e-2a557df42bf4
  Args:
    type: :Man
    source: Claus_von_Amsberg
  AssignClass (efc93719-fefc-4542-bdbf-34f02a35f47f)
 Call ID: efc93719-fefc-4542-bdbf-34f02a35f47f
  Args:
    source: Willem-Alexander
    type: :Man
  AssignClass (7b2b54ff-9243-4740-9b07-a2af520cb307)
 Call ID: 7b2b54ff-9243-4740-9b07-a2af520cb307
  Args:
    source: Johan_Friso
    type: :Man
  AssignClass (bc7c846a-5e85-4e4d-b0f4-445f3391cd22)
 Call ID: bc7c846a-5e85-4e4d-b0f4-445f3391cd22
  Args:
    type: :Woman
    source: Laurentien
  AssignClass (acdd25ac-a893-4b7e-ae77-e7e9a7f48e7e)
 Call ID: acdd25ac-a893-4b7e-ae77-e7e9a7f48e7e
  Args:
    source: Eloise
    type: :Woman
  AssignClass (c175497f-cc28-4202-a022-a5e24c3b9bdc)
 Call ID: c175497f-cc28-4202-a022-a5e24c3b9bdc
  Args:
    type: :Man
    source: Claus-Casimir
  AssignClass (f3aa34f3-f5d5-43ed-abda-618c12fec176)
 Call ID: f3aa34f3-f5d5-43ed-abda-618c12fec176
  Args:
    type: :Woman
    source: Leonore
  AddLiteral (675ec1aa-6b92-4a95-92f4-114192cf8eef)
 Call ID: 675ec1aa-6b92-4a95-92f4-114192cf8eef
  Args:
    literal_type: xsd:integer
    source: Constantijn
    relation: :hasBirthYear
    literal_value: 1969
  AddLiteral (77bc6ef7-3ec8-4664-bc3f-204a1eb5924f)
 Call ID: 77bc6ef7-3ec8-4664-bc3f-204a1eb5924f
  Args:
    source: Willem-Alexander
    literal_type: xsd:integer
    literal_value: 1967
    relation: :hasBirthYear
  AddLiteral (087fc601-5576-4557-9384-c624ebdf1fac)
 Call ID: 087fc601-5576-4557-9384-c624ebdf1fac
  Args:
    relation: :hasBirthYear
    literal_value: 1968
    literal_type: xsd:integer
    source: Johan_Friso
  AddLiteral (e5a6347d-80f6-4822-932a-e6666ff3bb81)
 Call ID: e5a6347d-80f6-4822-932a-e6666ff3bb81
  Args:
    source: Johan_Friso
    literal_type: xsd:integer
    literal_value: 2013
    relation: :hasDeathYear
  AddLiteral (936a30f9-6047-43a0-94fe-61cce37f823c)
 Call ID: 936a30f9-6047-43a0-94fe-61cce37f823c
  Args:
    relation: :hasBirthYear
    literal_value: 2002
    literal_type: xsd:integer
    source: Eloise
  AddLiteral (df0db60c-8854-4c5a-993b-f59477b9ddea)
 Call ID: df0db60c-8854-4c5a-993b-f59477b9ddea
  Args:
    relation: :hasBirthYear
    literal_value: 2004
    literal_type: xsd:integer
    source: Claus-Casimir
  AddLiteral (857db7e6-ccc4-4fbd-b04a-5f9838be7a77)
 Call ID: 857db7e6-ccc4-4fbd-b04a-5f9838be7a77
  Args:
    literal_value: 2006
    relation: :hasBirthYear
    source: Leonore
    literal_type: xsd:integer
  AddTriple (0901a57a-894d-455d-a686-7dda03f53028)
 Call ID: 0901a57a-894d-455d-a686-7dda03f53028
  Args:
    target: Beatrix
    relation: :hasMother
    source: Constantijn
  AddTriple (81dc6f94-4b48-441a-8b41-749d12e1d67f)
 Call ID: 81dc6f94-4b48-441a-8b41-749d12e1d67f
  Args:
    target: Claus_von_Amsberg
    relation: :hasFather
    source: Constantijn
  AddTriple (cd35c283-d9b7-426c-9e3d-a36317b5bdac)
 Call ID: cd35c283-d9b7-426c-9e3d-a36317b5bdac
  Args:
    target: Beatrix
    relation: :hasMother
    source: Willem-Alexander
  AddTriple (b4f5a5f3-ba26-4432-a3d4-5ff5eeec3e79)
 Call ID: b4f5a5f3-ba26-4432-a3d4-5ff5eeec3e79
  Args:
    source: Willem-Alexander
    relation: :hasFather
    target: Claus_von_Amsberg
  AddTriple (754d8fda-8b83-4323-a071-b8b109aebf2d)
 Call ID: 754d8fda-8b83-4323-a071-b8b109aebf2d
  Args:
    target: Beatrix
    relation: :hasMother
    source: Johan_Friso
  AddTriple (804d0a10-a5eb-4f64-94d4-d2d337727208)
 Call ID: 804d0a10-a5eb-4f64-94d4-d2d337727208
  Args:
    source: Johan_Friso
    target: Claus_von_Amsberg
    relation: :hasFather
  AddTriple (fd0dc5ff-fc8e-4bb4-8c34-2afb6465c13e)
 Call ID: fd0dc5ff-fc8e-4bb4-8c34-2afb6465c13e
  Args:
    source: Eloise
    target: Laurentien
    relation: :hasMother
  AddTriple (c5c1836b-0a0e-4306-b7e5-e400e70296ac)
 Call ID: c5c1836b-0a0e-4306-b7e5-e400e70296ac
  Args:
    source: Eloise
    target: Constantijn
    relation: :hasFather
  AddTriple (e2529028-f5f1-4472-99a6-f678bcbd2f31)
 Call ID: e2529028-f5f1-4472-99a6-f678bcbd2f31
  Args:
    target: Laurentien
    relation: :hasMother
    source: Claus-Casimir
  AddTriple (90ead549-4ce0-4d0c-b494-0f992e90b960)
 Call ID: 90ead549-4ce0-4d0c-b494-0f992e90b960
  Args:
    target: Constantijn
    relation: :hasFather
    source: Claus-Casimir
  AddTriple (9659d680-b73e-4c12-9a31-c26629036066)
 Call ID: 9659d680-b73e-4c12-9a31-c26629036066
  Args:
    source: Leonore
    target: Laurentien
    relation: :hasMother
  AddTriple (6de4ccc6-565e-4f49-bfb0-b0dc2f3bccd5)
 Call ID: 6de4ccc6-565e-4f49-bfb0-b0dc2f3bccd5
  Args:
    source: Leonore
    target: Constantijn
    relation: :hasFather
  Finish (0fa3c435-b24b-462d-98fd-25038033a340)
 Call ID: 0fa3c435-b24b-462d-98fd-25038033a340
  Args: