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
  AssignClass (958db5eb-3730-436e-b003-95fa025eadb5)
 Call ID: 958db5eb-3730-436e-b003-95fa025eadb5
  Args:
    type: :Woman
    source: Lady_Marina_Windsor
  AssignClass (e050965b-69fe-44a4-b6b8-2809b52a1106)
 Call ID: e050965b-69fe-44a4-b6b8-2809b52a1106
  Args:
    source: Lady_Marina_Windsor
    type: :Person
  AddLiteral (634fe7bb-5b24-4abb-b754-36da3cb63edb)
 Call ID: 634fe7bb-5b24-4abb-b754-36da3cb63edb
  Args:
    literal_type: xsd:integer
    literal_value: 1992
    relation: :hasBirthYear
    source: Lady_Marina_Windsor
  AssignClass (857a96f2-ff16-4d6d-9674-a82965f26fe2)
 Call ID: 857a96f2-ff16-4d6d-9674-a82965f26fe2
  Args:
    source: George_Windsor_Earl_of_St_Andrews
    type: :Man
  AssignClass (70234620-e61c-487d-8f50-0e82814e305c)
 Call ID: 70234620-e61c-487d-8f50-0e82814e305c
  Args:
    type: :Person
    source: George_Windsor_Earl_of_St_Andrews
  AssignClass (d9ba1341-a7ab-4aa4-b0b4-ad96c700cf1f)
 Call ID: d9ba1341-a7ab-4aa4-b0b4-ad96c700cf1f
  Args:
    source: Sylvana_Tomaselli
    type: :Woman
  AssignClass (3ae6b2e4-3452-4914-b99e-264157a3d03f)
 Call ID: 3ae6b2e4-3452-4914-b99e-264157a3d03f
  Args:
    source: Sylvana_Tomaselli
    type: :Person
  AddTriple (7a34f081-9bc4-4f05-89b0-aeeb4036d45b)
 Call ID: 7a34f081-9bc4-4f05-89b0-aeeb4036d45b
  Args:
    relation: :hasFather
    target: George_Windsor_Earl_of_St_Andrews
    source: Lady_Marina_Windsor
  AddTriple (2d112157-00d4-446b-869f-2931c12fda7f)
 Call ID: 2d112157-00d4-446b-869f-2931c12fda7f
  Args:
    target: Sylvana_Tomaselli
    source: Lady_Marina_Windsor
    relation: :hasMother
  AssignClass (a0b42f05-a652-4cbf-86c3-16d35a5f4e73)
 Call ID: a0b42f05-a652-4cbf-86c3-16d35a5f4e73
  Args:
    type: :Man
    source: Edward_Windsor_Lord_Downpatrick
  AssignClass (a61e0171-55a8-487e-a567-27097772caf2)
 Call ID: a61e0171-55a8-487e-a567-27097772caf2
  Args:
    type: :Person
    source: Edward_Windsor_Lord_Downpatrick
  AddTriple (0f990a6a-2329-4633-b30c-229bff6ffd78)
 Call ID: 0f990a6a-2329-4633-b30c-229bff6ffd78
  Args:
    target: Edward_Windsor_Lord_Downpatrick
    source: Lady_Marina_Windsor
    relation: :hasBrother
  AssignClass (52cacbcf-95e2-417d-b0dc-568ecb2480d5)
 Call ID: 52cacbcf-95e2-417d-b0dc-568ecb2480d5
  Args:
    source: Lady_Amelia_Windsor
    type: :Woman
  AssignClass (186d039e-2ae5-4bb0-a021-f05474465f78)
 Call ID: 186d039e-2ae5-4bb0-a021-f05474465f78
  Args:
    type: :Person
    source: Lady_Amelia_Windsor
  AddTriple (90fc7de2-d249-4c7a-b10f-7df41351be9d)
 Call ID: 90fc7de2-d249-4c7a-b10f-7df41351be9d
  Args:
    target: Lady_Amelia_Windsor
    source: Lady_Marina_Windsor
    relation: :hasSister
  AssignClass (561e82d1-6243-423b-af67-35161ed2927f)
 Call ID: 561e82d1-6243-423b-af67-35161ed2927f
  Args:
    type: :Man
    source: Prince_Edward_Duke_of_Kent
  AssignClass (fcab0a7c-c027-4520-ab81-1683d4caf761)
 Call ID: fcab0a7c-c027-4520-ab81-1683d4caf761
  Args:
    source: Prince_Edward_Duke_of_Kent
    type: :Person
  AssignClass (c30a25bd-8836-49c0-aa82-7532c3e0f740)
 Call ID: c30a25bd-8836-49c0-aa82-7532c3e0f740
  Args:
    type: :Woman
    source: Katharine_Duchess_of_Kent
  AssignClass (95a165e6-6b78-4171-b5d9-0860fa35ecf3)
 Call ID: 95a165e6-6b78-4171-b5d9-0860fa35ecf3
  Args:
    type: :Person
    source: Katharine_Duchess_of_Kent
  AddTriple (25fd7a35-639e-4c4c-a5bf-0a44f6927d8a)
 Call ID: 25fd7a35-639e-4c4c-a5bf-0a44f6927d8a
  Args:
    relation: :hasFather
    target: Prince_Edward_Duke_of_Kent
    source: George_Windsor_Earl_of_St_Andrews
  AddTriple (c00e7c17-eefb-4bdd-b30a-de5b970d13d1)
 Call ID: c00e7c17-eefb-4bdd-b30a-de5b970d13d1
  Args:
    relation: :hasMother
    target: Katharine_Duchess_of_Kent
    source: George_Windsor_Earl_of_St_Andrews
  AssignClass (6259f49f-493f-41b7-a340-e417ed8b5b7f)
 Call ID: 6259f49f-493f-41b7-a340-e417ed8b5b7f
  Args:
    type: :Man
    source: Sir_William_Worsley_4th_Baronet
  AssignClass (8481aac2-a5e1-4b72-8e68-7b6466eec351)
 Call ID: 8481aac2-a5e1-4b72-8e68-7b6466eec351
  Args:
    type: :Person
    source: Sir_William_Worsley_4th_Baronet
  AddTriple (b49b77f0-1e24-4114-927a-3df62ab9b761)
 Call ID: b49b77f0-1e24-4114-927a-3df62ab9b761
  Args:
    relation: :hasFather
    source: Katharine_Duchess_of_Kent
    target: Sir_William_Worsley_4th_Baronet
  AssignClass (72254d32-2393-4527-88bd-06a52d1f7515)
 Call ID: 72254d32-2393-4527-88bd-06a52d1f7515
  Args:
    type: :Woman
    source: Princess_Marina_of_Greece_and_Denmark
  AssignClass (5e6a5cd8-3be7-4570-815a-e8171f174a8f)
 Call ID: 5e6a5cd8-3be7-4570-815a-e8171f174a8f
  Args:
    source: Princess_Marina_of_Greece_and_Denmark
    type: :Person
  AssignClass (a273038e-16eb-46f1-809f-c89d3f3ed3fc)
 Call ID: a273038e-16eb-46f1-809f-c89d3f3ed3fc
  Args:
    type: :Woman
    source: Elizabeth_II
  AssignClass (7f971fc7-3924-47d9-b0a6-ac61182d0d3e)
 Call ID: 7f971fc7-3924-47d9-b0a6-ac61182d0d3e
  Args:
    source: Elizabeth_II
    type: :Person
  Finish (e3f25741-7c53-4b02-ba16-5845bc122942)
 Call ID: e3f25741-7c53-4b02-ba16-5845bc122942
  Args: