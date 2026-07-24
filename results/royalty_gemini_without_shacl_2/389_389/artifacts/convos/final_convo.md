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
Michael Claude Hamilton Bowes-Lyon (1 October 1893 – 1 May 1953), known as Mickie Bowes-Lyon, was an elder brother of Queen Elizabeth the Queen Mother and maternal uncle of Queen Elizabeth II.
Biography

Bowes-Lyon was born on 1 October 1893, the fifth son and eighth child of Claude Bowes-Lyon, Lord Glamis, later 14th
During World War I, Bowes-Lyon served in France in The Royal Scots (Lothian Regiment).
After the war, Bowes-Lyon was a justice of the peace and deputy lieutenant of Bedfordshire.
In 1928, Bowes-Lyon married Elizabeth Margaret Cator (1899–1959), daughter of John Cator, at St George's, Hanover Square.
Cator had been a bridesmaid at his sister Elizabeth's wedding to Prince Albert, Duke of York, in 1923.
Bowes-Lyon predeceased him and the earldom was inherited by his eldest son, Fergus, in 1972.
Bowes-Lyon died on 1 May 1953 at his home in Biggleswade as the result of asthma.



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
  AssignClass (f6fed113-22ef-4563-91e4-fdca41756b35)
 Call ID: f6fed113-22ef-4563-91e4-fdca41756b35
  Args:
    type: :Man
    source: :Michael_Claude_Hamilton_Bowes-Lyon
  AssignClass (ca2fa03c-9167-48b3-b79a-68fb79863630)
 Call ID: ca2fa03c-9167-48b3-b79a-68fb79863630
  Args:
    type: :Person
    source: :Michael_Claude_Hamilton_Bowes-Lyon
  AddLiteral (fe742c64-b723-474d-adf3-e94dad809a0c)
 Call ID: fe742c64-b723-474d-adf3-e94dad809a0c
  Args:
    relation: :knownAs
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    literal_value: Mickie Bowes-Lyon
    literal_type: xsd:string
  AddLiteral (15acf61e-1dc6-493a-94d0-b896bd35c860)
 Call ID: 15acf61e-1dc6-493a-94d0-b896bd35c860
  Args:
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    literal_value: 1893
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (72d4a1da-0ba9-48ed-99d3-5269f14b5a8a)
 Call ID: 72d4a1da-0ba9-48ed-99d3-5269f14b5a8a
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    literal_value: 1953
  AssignClass (c317bc5e-8a75-48c7-b894-fb4d3c897692)
 Call ID: c317bc5e-8a75-48c7-b894-fb4d3c897692
  Args:
    type: :Man
    source: :Claude_Bowes-Lyon
  AssignClass (5321da63-e822-4c9f-ab09-06aaa362b03c)
 Call ID: 5321da63-e822-4c9f-ab09-06aaa362b03c
  Args:
    type: :Person
    source: :Claude_Bowes-Lyon
  AddTriple (d202a370-73ed-4821-9420-c82c0fdbce8f)
 Call ID: d202a370-73ed-4821-9420-c82c0fdbce8f
  Args:
    target: :Michael_Claude_Hamilton_Bowes-Lyon
    source: :Claude_Bowes-Lyon
    relation: :isFatherOf
  AssignClass (ae420eba-6a7e-4b7b-8aa5-376c22b6367e)
 Call ID: ae420eba-6a7e-4b7b-8aa5-376c22b6367e
  Args:
    type: :Woman
    source: :Elizabeth_Bowes-Lyon
  AssignClass (a7582cc1-025d-4024-8ff3-79009d6e89dc)
 Call ID: a7582cc1-025d-4024-8ff3-79009d6e89dc
  Args:
    source: :Elizabeth_Bowes-Lyon
    type: :Person
  AddTriple (0244f245-a54f-49be-9484-1300b39476b6)
 Call ID: 0244f245-a54f-49be-9484-1300b39476b6
  Args:
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    relation: :isSiblingOf
    target: :Elizabeth_Bowes-Lyon
  AssignClass (7339b7d3-4b12-4905-a4d9-0e2179cac351)
 Call ID: 7339b7d3-4b12-4905-a4d9-0e2179cac351
  Args:
    type: :Woman
    source: :Queen_Elizabeth_II
  AssignClass (59b32f11-3e48-4b7d-8d95-355999ed91a1)
 Call ID: 59b32f11-3e48-4b7d-8d95-355999ed91a1
  Args:
    type: :Person
    source: :Queen_Elizabeth_II
  AddTriple (965212ba-b878-4983-9a73-651b82751575)
 Call ID: 965212ba-b878-4983-9a73-651b82751575
  Args:
    target: :Queen_Elizabeth_II
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    relation: :isUncleOf
  AssignClass (11b63201-91a5-49eb-ae57-27379bf65189)
 Call ID: 11b63201-91a5-49eb-ae57-27379bf65189
  Args:
    type: :Woman
    source: :Elizabeth_Margaret_Cator
  AssignClass (b6d27d1f-f1c0-4c0d-9148-69281258920f)
 Call ID: b6d27d1f-f1c0-4c0d-9148-69281258920f
  Args:
    source: :Elizabeth_Margaret_Cator
    type: :Person
  AddLiteral (e465b15b-85d3-456a-81f1-6d331c2599c8)
 Call ID: e465b15b-85d3-456a-81f1-6d331c2599c8
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1928
    source: :Michael_Claude_Hamilton_Bowes-Lyon
  AddTriple (124122b2-6341-4c37-81d1-460f4cc3b400)
 Call ID: 124122b2-6341-4c37-81d1-460f4cc3b400
  Args:
    target: :Elizabeth_Margaret_Cator
    relation: :hasRelation
    source: :Michael_Claude_Hamilton_Bowes-Lyon
  AssignClass (83527b56-c794-413e-bd6b-5efb6d801267)
 Call ID: 83527b56-c794-413e-bd6b-5efb6d801267
  Args:
    source: :John_Cator
    type: :Man
  AssignClass (4e0d6a87-aa1e-48be-9390-5829ab4ae0a4)
 Call ID: 4e0d6a87-aa1e-48be-9390-5829ab4ae0a4
  Args:
    type: :Person
    source: :John_Cator
  AddTriple (8137e4b4-b030-4a31-87cb-cf57e6cad2a2)
 Call ID: 8137e4b4-b030-4a31-87cb-cf57e6cad2a2
  Args:
    target: :Elizabeth_Margaret_Cator
    relation: :isFatherOf
    source: :John_Cator
  AssignClass (6bb0147e-337c-4358-87bd-cf3dcdd4b000)
 Call ID: 6bb0147e-337c-4358-87bd-cf3dcdd4b000
  Args:
    source: :Fergus_Bowes-Lyon
    type: :Man
  AssignClass (cc632892-79c3-4aec-a920-91fd1ef7ae43)
 Call ID: cc632892-79c3-4aec-a920-91fd1ef7ae43
  Args:
    source: :Fergus_Bowes-Lyon
    type: :Person
  AddTriple (a8e305c9-1575-4e2c-8c0c-32672a2ed2b4)
 Call ID: a8e305c9-1575-4e2c-8c0c-32672a2ed2b4
  Args:
    source: :Fergus_Bowes-Lyon
    relation: :isSonOf
    target: :Michael_Claude_Hamilton_Bowes-Lyon
  Finish (209439f7-6872-4ec1-b800-adab891ee73e)
 Call ID: 209439f7-6872-4ec1-b800-adab891ee73e
  Args: