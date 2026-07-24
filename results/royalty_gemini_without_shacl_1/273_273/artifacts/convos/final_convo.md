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
Lady Marina Charlotte
Alexandra Katharine Helen Windsor (born 30 September 1992) is a British philanthropic executive and relative of the British royal family.
Early life, family, and education

Lady Marina Charlotte
Alexandra Katharine Helen Windsor was born on 30 September 1992 at the Rosie Hospital in Cambridge, Cambridgeshire, the second child of George Windsor, Earl of St Andrews, a diplomat and member of the House of Windsor, and Sylvana Tomaselli, a Canadian historian and member of the Austrian-Italian Tomaselli family.
Her older brother is Edward Windsor, Lord Downpatrick, and her younger sister is Lady Amelia Windsor.
She is a paternal granddaughter of Prince Edward, Duke of Kent, who is a first cousin of Elizabeth II, and Katharine, Duchess of Kent, the only daughter of Sir William Worsley, 4th Baronet.
Marina is named after her great-grandmother Princess Marina of Greece and Denmark.
On 21 January 1993, Marina was christened Marina Charlotte
Alexandra Katharine Helen Windsor in a Church of England ceremony by William Booth, the sub-dean of the Chapel Royal at St James's Palace.
Her godparents are Lady Ralph Kerr, Katherine Ruth Panter, William Hanbury-Tenison, and Sasha Poklewski-Koziell.
Marina attended St Mary's School, Ascot, a Roman Catholic boarding school for girls.
Succession rights

Until 2008, Marina was 25th in the line of succession to the British throne.
, Marina modelled for Hardy Amies in Tatler alongside her siblings.
Personal life

She attended the wedding of her third cousin Prince William, Duke of Cambridge to Catherine Middleton in 2011.
In May 2012, Marina travelled to Thailand, where she trained in Muay Thai boxing.



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
  AssignClass (4d59edf3-f263-4d7b-b07f-6d3b81771e4a)
 Call ID: 4d59edf3-f263-4d7b-b07f-6d3b81771e4a
  Args:
    type: :Woman
    source: Lady_Marina_Windsor
  AssignClass (91575ea5-9765-4f6c-964c-d37d5c6e0920)
 Call ID: 91575ea5-9765-4f6c-964c-d37d5c6e0920
  Args:
    type: :Person
    source: Lady_Marina_Windsor
  AddLiteral (bae3c04b-1b67-4925-b58b-c3663274f63c)
 Call ID: bae3c04b-1b67-4925-b58b-c3663274f63c
  Args:
    literal_type: xsd:integer
    source: Lady_Marina_Windsor
    relation: :hasBirthYear
    literal_value: 1992
  AssignClass (e424be09-8a7c-4fde-b562-2abfb667b133)
 Call ID: e424be09-8a7c-4fde-b562-2abfb667b133
  Args:
    type: :Man
    source: George_Windsor
  AssignClass (6b1cdb1a-d5cd-442f-93fe-450341809c97)
 Call ID: 6b1cdb1a-d5cd-442f-93fe-450341809c97
  Args:
    type: :Person
    source: George_Windsor
  AssignClass (6cbf1f74-81ba-4257-b667-3f90b0fbfe2e)
 Call ID: 6cbf1f74-81ba-4257-b667-3f90b0fbfe2e
  Args:
    type: :Woman
    source: Sylvana_Tomaselli
  AssignClass (1509899d-04c5-4bb1-96f7-61b67744734e)
 Call ID: 1509899d-04c5-4bb1-96f7-61b67744734e
  Args:
    type: :Person
    source: Sylvana_Tomaselli
  AddTriple (deff26c1-72c3-4bf4-a76e-f955ae006638)
 Call ID: deff26c1-72c3-4bf4-a76e-f955ae006638
  Args:
    source: Lady_Marina_Windsor
    relation: :hasFather
    target: George_Windsor
  AddTriple (98939418-5dc3-4fdd-8c9e-7239dceab1e8)
 Call ID: 98939418-5dc3-4fdd-8c9e-7239dceab1e8
  Args:
    target: Sylvana_Tomaselli
    source: Lady_Marina_Windsor
    relation: :hasMother
  AssignClass (cf2f956b-edc1-4f73-8778-a57fa40f9795)
 Call ID: cf2f956b-edc1-4f73-8778-a57fa40f9795
  Args:
    type: :Man
    source: Edward_Windsor
  AssignClass (9ef4a6a4-d51f-4c35-80f3-a0a52213a842)
 Call ID: 9ef4a6a4-d51f-4c35-80f3-a0a52213a842
  Args:
    type: :Person
    source: Edward_Windsor
  AddTriple (1f63d068-7a50-4d10-ac1c-f2b5ccb028b5)
 Call ID: 1f63d068-7a50-4d10-ac1c-f2b5ccb028b5
  Args:
    source: Lady_Marina_Windsor
    relation: :isSiblingOf
    target: Edward_Windsor
  AssignClass (bdaa74f0-d128-44cf-a81d-4ab868c960b6)
 Call ID: bdaa74f0-d128-44cf-a81d-4ab868c960b6
  Args:
    type: :Woman
    source: Lady_Amelia_Windsor
  AssignClass (16c4ca23-8124-424e-aee4-ceefa1c8b6e5)
 Call ID: 16c4ca23-8124-424e-aee4-ceefa1c8b6e5
  Args:
    type: :Person
    source: Lady_Amelia_Windsor
  AddTriple (040eebd2-bb20-49bc-b80d-5250323d9605)
 Call ID: 040eebd2-bb20-49bc-b80d-5250323d9605
  Args:
    source: Lady_Marina_Windsor
    relation: :isSiblingOf
    target: Lady_Amelia_Windsor
  AssignClass (3d3114d2-759a-4db1-b479-2026a7a463d3)
 Call ID: 3d3114d2-759a-4db1-b479-2026a7a463d3
  Args:
    type: :Man
    source: Prince_Edward_Duke_of_Kent
  AssignClass (411d364a-cfbe-4e59-9c0d-ac7c51c348d3)
 Call ID: 411d364a-cfbe-4e59-9c0d-ac7c51c348d3
  Args:
    type: :Person
    source: Prince_Edward_Duke_of_Kent
  AssignClass (c91ab01f-ad3c-42f4-9389-964944943946)
 Call ID: c91ab01f-ad3c-42f4-9389-964944943946
  Args:
    type: :Woman
    source: Katharine_Duchess_of_Kent
  AssignClass (a8b480e7-8a1a-411a-90cd-08c097fec096)
 Call ID: a8b480e7-8a1a-411a-90cd-08c097fec096
  Args:
    type: :Person
    source: Katharine_Duchess_of_Kent
  AddTriple (43d715f0-5cb0-4668-b9e8-ed691b5dbfa2)
 Call ID: 43d715f0-5cb0-4668-b9e8-ed691b5dbfa2
  Args:
    relation: :hasFather
    source: George_Windsor
    target: Prince_Edward_Duke_of_Kent
  AddTriple (11f7f3c8-ce66-4d85-b0a4-1469ff3c93da)
 Call ID: 11f7f3c8-ce66-4d85-b0a4-1469ff3c93da
  Args:
    target: Katharine_Duchess_of_Kent
    relation: :hasMother
    source: George_Windsor
  AssignClass (536e4979-99d6-40fa-8a87-1f0beecf8da8)
 Call ID: 536e4979-99d6-40fa-8a87-1f0beecf8da8
  Args:
    type: :Man
    source: Sir_William_Worsley
  AssignClass (12736ba7-ab95-4892-a82b-43a424f918ce)
 Call ID: 12736ba7-ab95-4892-a82b-43a424f918ce
  Args:
    type: :Person
    source: Sir_William_Worsley
  AddTriple (7338cd27-968d-43a3-abcf-1c740300452d)
 Call ID: 7338cd27-968d-43a3-abcf-1c740300452d
  Args:
    source: Katharine_Duchess_of_Kent
    relation: :hasFather
    target: Sir_William_Worsley
  AssignClass (2d1ff297-c53a-47ed-a8a3-4dba36d251db)
 Call ID: 2d1ff297-c53a-47ed-a8a3-4dba36d251db
  Args:
    type: :Woman
    source: Princess_Marina_of_Greece_and_Denmark
  AssignClass (c8d180eb-171d-4acd-9333-8875e9cd4c38)
 Call ID: c8d180eb-171d-4acd-9333-8875e9cd4c38
  Args:
    type: :Person
    source: Princess_Marina_of_Greece_and_Denmark
  Finish (a769be96-1cef-446a-86e7-0dedd13d88a4)
 Call ID: a769be96-1cef-446a-86e7-0dedd13d88a4
  Args: