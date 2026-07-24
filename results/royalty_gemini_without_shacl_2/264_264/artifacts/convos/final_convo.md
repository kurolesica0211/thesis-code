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
  AssignClass (f7418a0a-bac7-4635-a8fc-5e3990301d81)
 Call ID: f7418a0a-bac7-4635-a8fc-5e3990301d81
  Args:
    source: Beatrix
    type: :Woman
  AssignClass (742d846b-0e7b-4290-b952-612ffcfadbdb)
 Call ID: 742d846b-0e7b-4290-b952-612ffcfadbdb
  Args:
    type: :Woman
    source: Margriet
  AssignClass (078216cf-7069-4970-acab-6efb17675ec5)
 Call ID: 078216cf-7069-4970-acab-6efb17675ec5
  Args:
    source: Pieter_van_Vollenhoven
    type: :Man
  AssignClass (af26d865-c402-4663-82d2-46ab7314226f)
 Call ID: af26d865-c402-4663-82d2-46ab7314226f
  Args:
    type: :Man
    source: Constantijn
  AddLiteral (b3e835c5-2c0f-4490-b09c-1499d6d050a7)
 Call ID: b3e835c5-2c0f-4490-b09c-1499d6d050a7
  Args:
    source: Constantijn
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    literal_value: 1969
  AddTriple (290f94f4-b109-4806-9665-608f11d93713)
 Call ID: 290f94f4-b109-4806-9665-608f11d93713
  Args:
    relation: :hasMother
    target: Beatrix
    source: Constantijn
  AddTriple (fe10173c-9054-4d32-894b-36f7b531c7ea)
 Call ID: fe10173c-9054-4d32-894b-36f7b531c7ea
  Args:
    target: Claus_von_Amsberg
    source: Constantijn
    relation: :hasFather
  AssignClass (edb6a989-de9e-4e1e-8848-185fca02ee02)
 Call ID: edb6a989-de9e-4e1e-8848-185fca02ee02
  Args:
    type: :Man
    source: Claus_von_Amsberg
  AddTriple (fe109e50-aceb-4102-9d53-e71ef4b73563)
 Call ID: fe109e50-aceb-4102-9d53-e71ef4b73563
  Args:
    relation: :isBrotherOf
    target: Willem-Alexander
    source: Constantijn
  AssignClass (955eeb74-b6c3-4e20-92c9-015ab2cb29d6)
 Call ID: 955eeb74-b6c3-4e20-92c9-015ab2cb29d6
  Args:
    source: Willem-Alexander
    type: :Man
  AddLiteral (3b4aec2e-24e6-4118-8f2d-667957530a7e)
 Call ID: 3b4aec2e-24e6-4118-8f2d-667957530a7e
  Args:
    literal_value: 1967
    source: Willem-Alexander
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
  AssignClass (d182b8c3-ed90-416f-8099-f9ad8e217b24)
 Call ID: d182b8c3-ed90-416f-8099-f9ad8e217b24
  Args:
    source: Johan_Friso
    type: :Man
  AddLiteral (2b8926fe-dd13-460a-9c2e-8a3eddcb406a)
 Call ID: 2b8926fe-dd13-460a-9c2e-8a3eddcb406a
  Args:
    literal_type: xsd:positiveInteger
    source: Johan_Friso
    relation: :hasBirthYear
    literal_value: 1968
  AddLiteral (c2575daf-792d-4298-a0fa-110b1d19f6fb)
 Call ID: c2575daf-792d-4298-a0fa-110b1d19f6fb
  Args:
    relation: :hasDeathYear
    source: Johan_Friso
    literal_type: xsd:positiveInteger
    literal_value: 2013
  AddTriple (5fc0d75c-120b-4088-9fff-6202cb41804f)
 Call ID: 5fc0d75c-120b-4088-9fff-6202cb41804f
  Args:
    relation: :isBrotherOf
    target: Johan_Friso
    source: Constantijn
  AssignClass (986b09c3-219b-4435-b841-3f02c7036034)
 Call ID: 986b09c3-219b-4435-b841-3f02c7036034
  Args:
    source: Laurentien_Brinkhorst
    type: :Woman
  AddTriple (bfdaaac2-1d0d-4479-9542-6cbb0dfce66a)
 Call ID: bfdaaac2-1d0d-4479-9542-6cbb0dfce66a
  Args:
    source: Eloise
    target: Constantijn
    relation: :hasFather
  AddTriple (e1e0a78e-e91b-439a-a28b-b9d7906f7371)
 Call ID: e1e0a78e-e91b-439a-a28b-b9d7906f7371
  Args:
    relation: :hasMother
    source: Eloise
    target: Laurentien_Brinkhorst
  AssignClass (f7a037fb-07a0-4b51-8084-34d66a13ece0)
 Call ID: f7a037fb-07a0-4b51-8084-34d66a13ece0
  Args:
    source: Eloise
    type: :Woman
  AddLiteral (4f31cb3d-44df-496a-bb8f-2d58856f29d8)
 Call ID: 4f31cb3d-44df-496a-bb8f-2d58856f29d8
  Args:
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    source: Eloise
    literal_value: 2002
  AddTriple (ebd00f3c-7267-45a7-908a-9345f6be67c4)
 Call ID: ebd00f3c-7267-45a7-908a-9345f6be67c4
  Args:
    target: Constantijn
    source: Claus-Casimir
    relation: :hasFather
  AddTriple (fdb3a741-b984-4546-983e-de086c12dd85)
 Call ID: fdb3a741-b984-4546-983e-de086c12dd85
  Args:
    target: Laurentien_Brinkhorst
    source: Claus-Casimir
    relation: :hasMother
  AssignClass (a3361b6c-7ad1-42b8-be43-5ed5a1cf5d12)
 Call ID: a3361b6c-7ad1-42b8-be43-5ed5a1cf5d12
  Args:
    type: :Man
    source: Claus-Casimir
  AddLiteral (b1cc7669-1dc8-4ac0-95a1-db031ea87728)
 Call ID: b1cc7669-1dc8-4ac0-95a1-db031ea87728
  Args:
    literal_value: 2004
    literal_type: xsd:positiveInteger
    source: Claus-Casimir
    relation: :hasBirthYear
  AddTriple (ff63e9ae-a8a2-4792-aff6-38b9638f17c6)
 Call ID: ff63e9ae-a8a2-4792-aff6-38b9638f17c6
  Args:
    relation: :hasFather
    source: Leonore
    target: Constantijn
  AddTriple (2d0fea1d-bf30-4283-a5b2-89fd39c401c6)
 Call ID: 2d0fea1d-bf30-4283-a5b2-89fd39c401c6
  Args:
    source: Leonore
    target: Laurentien_Brinkhorst
    relation: :hasMother
  AssignClass (7d0fdfc8-691a-41ba-bdde-3cdf482a480f)
 Call ID: 7d0fdfc8-691a-41ba-bdde-3cdf482a480f
  Args:
    type: :Woman
    source: Leonore
  AddLiteral (dff47b9b-6886-4d35-ab42-9393e8028c4d)
 Call ID: dff47b9b-6886-4d35-ab42-9393e8028c4d
  Args:
    literal_value: 2006
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    source: Leonore
  Finish (0d72423d-404b-4241-8e30-0e1f400ad3ff)
 Call ID: 0d72423d-404b-4241-8e30-0e1f400ad3ff
  Args: