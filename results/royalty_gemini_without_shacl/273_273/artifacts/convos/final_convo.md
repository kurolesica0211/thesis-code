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
  AssignClass (6526097b-2066-48f7-bf5d-9eec23d5e6b3)
 Call ID: 6526097b-2066-48f7-bf5d-9eec23d5e6b3
  Args:
    type: :Woman
    source: :Lady_Marina_Charlotte_Alexandra_Katharine_Helen_Windsor
  AssignClass (7bbc6881-35c4-4c61-9ab4-2ba144cdafbe)
 Call ID: 7bbc6881-35c4-4c61-9ab4-2ba144cdafbe
  Args:
    source: :Lady_Marina_Charlotte_Alexandra_Katharine_Helen_Windsor
    type: :Person
  AddLiteral (ae4408c9-f62e-4236-829a-949cd8e44a89)
 Call ID: ae4408c9-f62e-4236-829a-949cd8e44a89
  Args:
    source: :Lady_Marina_Charlotte_Alexandra_Katharine_Helen_Windsor
    relation: :hasBirthYear
    literal_value: 1992
    literal_type: xsd:integer
  AssignClass (bff0b11b-0b42-4f59-986b-9bfb7ee1d2b4)
 Call ID: bff0b11b-0b42-4f59-986b-9bfb7ee1d2b4
  Args:
    type: :Man
    source: :George_Windsor_Earl_of_St_Andrews
  AssignClass (c498f2c8-d55b-40c8-ba3e-0dfb0eda5512)
 Call ID: c498f2c8-d55b-40c8-ba3e-0dfb0eda5512
  Args:
    source: :George_Windsor_Earl_of_St_Andrews
    type: :Person
  AssignClass (c7c558d7-b812-4e81-a6a4-66171ba603c5)
 Call ID: c7c558d7-b812-4e81-a6a4-66171ba603c5
  Args:
    type: :Woman
    source: :Sylvana_Tomaselli
  AssignClass (e0b932b6-862b-48b2-84e4-764459102a9d)
 Call ID: e0b932b6-862b-48b2-84e4-764459102a9d
  Args:
    type: :Person
    source: :Sylvana_Tomaselli
  AddTriple (8d4f8067-a247-4306-94d3-3b02cfca3767)
 Call ID: 8d4f8067-a247-4306-94d3-3b02cfca3767
  Args:
    relation: :hasFather
    target: :George_Windsor_Earl_of_St_Andrews
    source: :Lady_Marina_Charlotte_Alexandra_Katharine_Helen_Windsor
  AddTriple (fbfe1e72-46b0-412f-b1e4-2e33fb44f68f)
 Call ID: fbfe1e72-46b0-412f-b1e4-2e33fb44f68f
  Args:
    source: :Lady_Marina_Charlotte_Alexandra_Katharine_Helen_Windsor
    target: :Sylvana_Tomaselli
    relation: :hasMother
  AssignClass (a05493c4-c905-42b3-8785-62681729b394)
 Call ID: a05493c4-c905-42b3-8785-62681729b394
  Args:
    source: :Edward_Windsor_Lord_Downpatrick
    type: :Man
  AssignClass (6254b68a-9300-42db-82df-bf82a5f2b55f)
 Call ID: 6254b68a-9300-42db-82df-bf82a5f2b55f
  Args:
    source: :Edward_Windsor_Lord_Downpatrick
    type: :Person
  AddTriple (3f5294c3-1792-4b3e-acc1-ff2191b98f36)
 Call ID: 3f5294c3-1792-4b3e-acc1-ff2191b98f36
  Args:
    source: :Lady_Marina_Charlotte_Alexandra_Katharine_Helen_Windsor
    target: :Edward_Windsor_Lord_Downpatrick
    relation: :hasBrother
  AssignClass (d4c03ab0-e6f4-46af-844d-eb612f71b667)
 Call ID: d4c03ab0-e6f4-46af-844d-eb612f71b667
  Args:
    source: :Lady_Amelia_Windsor
    type: :Woman
  AssignClass (35acdfc5-9e81-4bd0-a8c3-112558556d93)
 Call ID: 35acdfc5-9e81-4bd0-a8c3-112558556d93
  Args:
    type: :Person
    source: :Lady_Amelia_Windsor
  AddTriple (ceb1e8f0-32ff-4580-be3d-42d899f3ce70)
 Call ID: ceb1e8f0-32ff-4580-be3d-42d899f3ce70
  Args:
    source: :Lady_Marina_Charlotte_Alexandra_Katharine_Helen_Windsor
    relation: :hasSister
    target: :Lady_Amelia_Windsor
  AssignClass (e1e8c48a-9644-49d6-bac0-573bea493d13)
 Call ID: e1e8c48a-9644-49d6-bac0-573bea493d13
  Args:
    source: :Prince_Edward_Duke_of_Kent
    type: :Man
  AssignClass (3f062f5d-6d3f-4d68-8571-ecd19b872698)
 Call ID: 3f062f5d-6d3f-4d68-8571-ecd19b872698
  Args:
    type: :Person
    source: :Prince_Edward_Duke_of_Kent
  AssignClass (b0eb6eb5-3b61-4ce7-928a-f6018a5f088a)
 Call ID: b0eb6eb5-3b61-4ce7-928a-f6018a5f088a
  Args:
    type: :Woman
    source: :Katharine_Duchess_of_Kent
  AssignClass (7b28741f-46ec-4559-84e6-0e66b6383ecc)
 Call ID: 7b28741f-46ec-4559-84e6-0e66b6383ecc
  Args:
    type: :Person
    source: :Katharine_Duchess_of_Kent
  AddTriple (b18c2dfc-2072-41a8-80a5-ac6fb04011e9)
 Call ID: b18c2dfc-2072-41a8-80a5-ac6fb04011e9
  Args:
    source: :George_Windsor_Earl_of_St_Andrews
    relation: :hasFather
    target: :Prince_Edward_Duke_of_Kent
  AddTriple (d55a667b-cc3f-479e-92e6-f759d358a0cb)
 Call ID: d55a667b-cc3f-479e-92e6-f759d358a0cb
  Args:
    relation: :hasMother
    target: :Katharine_Duchess_of_Kent
    source: :George_Windsor_Earl_of_St_Andrews
  AssignClass (c8247994-806a-4bcb-919e-77f11a648d0b)
 Call ID: c8247994-806a-4bcb-919e-77f11a648d0b
  Args:
    type: :Man
    source: :Sir_William_Worsley_4th_Baronet
  AssignClass (42b1cf36-d2aa-429f-bb01-e14dcf17a07e)
 Call ID: 42b1cf36-d2aa-429f-bb01-e14dcf17a07e
  Args:
    type: :Person
    source: :Sir_William_Worsley_4th_Baronet
  AddTriple (e55e02cd-67f0-4b22-9006-b753ebdd3faa)
 Call ID: e55e02cd-67f0-4b22-9006-b753ebdd3faa
  Args:
    relation: :hasFather
    target: :Sir_William_Worsley_4th_Baronet
    source: :Katharine_Duchess_of_Kent
  Finish (a22bee77-0613-4dda-ab92-37b5fc53b8ee)
 Call ID: a22bee77-0613-4dda-ab92-37b5fc53b8ee
  Args: