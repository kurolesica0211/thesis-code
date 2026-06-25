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
Prince Ferdinand Pius (Ferdinando Pio Maria), Duke of Calabria and Castro (25 July 1869, Rome – 7 January 1960, Lindau), was head of the House of Bourbon-Two Sicilies and pretender to the throne of the extinct Kingdom of the Two Sicilies from 1934 to 1960.
Family

Ferdinand was the eldest child of Prince Alfonso, Count of Caserta and his wife Princess Maria Antonietta of Bourbon-Two Sicilies.
He was a grandson of Ferdinand II of the Two Sicilies and an older brother of Prince Carlos of Bourbon-Two Sicilies, Maria Immaculata, Princess Johann Georg of Saxony, Maria Cristina, Archduchess Peter Ferdinand of Austria, Maria di Grazia, Princess Imperial of Brazil, Prince Ranieri, Duke of Castro, Prince Philip of Bourbon-Two Sicilies, and Prince Gabriel of Bourbon-Two Sicilies.
Marriage

Ferdinand married Princess Maria Ludwiga Theresia of Bavaria, daughter of King Ludwig III of Bavaria on 31 May 1897.
They had six children:


Ferdinand and Maria lived for many years at Villa Amsee, Lindau.
Disputed succession

Following Ferdinand's death, the headship of the House of Bourbon-Two Sicilies was claimed by both his nephew Infante Alfonso, Duke of Calabria, and his brother Prince Ranieri, Duke of Castro, and remains disputed between their descendants.
The basis of Alfonso’s claim was that his late father, Prince Carlos of Bourbon-Two Sicilies (1870–1949), had been Ferdinand's next oldest brother.
But Henri, Count of Paris, upheld the claim of Ferdinand's younger brother, Prince Ranieri, Duke of Castro (1883–1973), contending that Carlos had renounced his rights of succession for himself and his descendants in 1901 when he married the Spanish heiress presumptive María de las Mercedes, Princess of Asturias.
The Count of Paris was well aware that his own claim to the French throne depended on the validity of the renunciation in 1713 of Philip V of Spain, in favor of the junior House of Orléans.
In 1900, Prince Carlos had executed the Act of Cannes, in anticipation of his marriage to María de las Mercedes, and in 1901 he became a Spanish subject and accepted the title of Infante.
The position of Ranieri was that by so doing Carlos had renounced any claim to the throne of the Two Sicilies.
But Alfonso had a different interpretation, which was that the Act of Cannes would have taken effect only if Mercedes and Carlos had succeeded to the Spanish throne.
He also argued that the Act of Cannes was invalid under the succession rules of the house of Two Sicilies.
Military service

Ferdinand initially served in the Spanish Army, and after leaving service held the honorary rank of Comandante of the General Staff of the Spanish Army.
Feld-Artillerie-Regiment "Prinz Ferdinand von Bourbon, Herzog von Calabrien"), which was renamed in honor of him.



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
  AssignClass (4827161f-3dd8-4831-b945-fa5a6d37cec6)
 Call ID: 4827161f-3dd8-4831-b945-fa5a6d37cec6
  Args:
    type: :Man
    source: :FerdinandPius
  AssignClass (2c9875e2-fafb-4592-b65d-bb6797f8d00a)
 Call ID: 2c9875e2-fafb-4592-b65d-bb6797f8d00a
  Args:
    type: :Person
    source: :FerdinandPius
  AddLiteral (708350c3-8313-4337-8531-82add2fa744c)
 Call ID: 708350c3-8313-4337-8531-82add2fa744c
  Args:
    relation: :hasBirthYear
    literal_value: 1869
    literal_type: xsd:integer
    source: :FerdinandPius
  AddLiteral (18583181-f5c3-4cec-8029-8f120399ff6a)
 Call ID: 18583181-f5c3-4cec-8029-8f120399ff6a
  Args:
    source: :FerdinandPius
    literal_type: xsd:integer
    literal_value: 1960
    relation: :hasDeathYear
  AssignClass (02ea13e2-e306-4a5f-a49d-66b2dacf82fc)
 Call ID: 02ea13e2-e306-4a5f-a49d-66b2dacf82fc
  Args:
    type: :Man
    source: :AlfonsoCountOfCaserta
  AssignClass (aaffaae7-e75c-44f5-a8d8-68cbc634a431)
 Call ID: aaffaae7-e75c-44f5-a8d8-68cbc634a431
  Args:
    source: :AlfonsoCountOfCaserta
    type: :Person
  AddTriple (fe0a18a9-fc24-475d-a48c-8ac092990824)
 Call ID: fe0a18a9-fc24-475d-a48c-8ac092990824
  Args:
    relation: :hasFather
    target: :AlfonsoCountOfCaserta
    source: :FerdinandPius
  AssignClass (2e657919-b760-41ef-87f2-927b7a51779d)
 Call ID: 2e657919-b760-41ef-87f2-927b7a51779d
  Args:
    source: :MariaAntonietta
    type: :Woman
  AssignClass (e4ab1542-5b68-4da9-98dd-de36121754ff)
 Call ID: e4ab1542-5b68-4da9-98dd-de36121754ff
  Args:
    type: :Person
    source: :MariaAntonietta
  AddTriple (61275a58-a37c-44f1-8201-758b1bc034f0)
 Call ID: 61275a58-a37c-44f1-8201-758b1bc034f0
  Args:
    source: :FerdinandPius
    target: :MariaAntonietta
    relation: :hasMother
  AssignClass (32536d69-020f-4306-9d34-355564fe1308)
 Call ID: 32536d69-020f-4306-9d34-355564fe1308
  Args:
    source: :FerdinandII
    type: :Man
  AssignClass (c283d91d-7f93-4112-9795-ec11e5a753cc)
 Call ID: c283d91d-7f93-4112-9795-ec11e5a753cc
  Args:
    type: :Person
    source: :FerdinandII
  AddTriple (c498f411-df2a-4ea4-9387-9f58a2acea23)
 Call ID: c498f411-df2a-4ea4-9387-9f58a2acea23
  Args:
    relation: :hasFather
    source: :AlfonsoCountOfCaserta
    target: :FerdinandII
  AssignClass (70bb1fd8-7a4c-41aa-ba88-7bf664d8b560)
 Call ID: 70bb1fd8-7a4c-41aa-ba88-7bf664d8b560
  Args:
    source: :MariaLudwigaTheresia
    type: :Woman
  AssignClass (1dfa6b63-788e-4de9-b767-ffedded0dedc)
 Call ID: 1dfa6b63-788e-4de9-b767-ffedded0dedc
  Args:
    type: :Person
    source: :MariaLudwigaTheresia
  AddTriple (601b1a2e-8141-4ac4-b594-8a34b39c88c9)
 Call ID: 601b1a2e-8141-4ac4-b594-8a34b39c88c9
  Args:
    relation: :hasRelation
    source: :FerdinandPius
    target: :MariaLudwigaTheresia
  AddLiteral (55c7714f-5dfc-4850-8cd7-58227fdeba53)
 Call ID: 55c7714f-5dfc-4850-8cd7-58227fdeba53
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1897
    source: :FerdinandPius
  AssignClass (78117049-61a3-40d8-a788-d03ed534e9d3)
 Call ID: 78117049-61a3-40d8-a788-d03ed534e9d3
  Args:
    type: :Man
    source: :LudwigIII
  AssignClass (729cc576-0497-43f2-8667-6089892ff586)
 Call ID: 729cc576-0497-43f2-8667-6089892ff586
  Args:
    source: :LudwigIII
    type: :Person
  AddTriple (4481b2b9-6a0f-4015-af63-df02cf07a0f7)
 Call ID: 4481b2b9-6a0f-4015-af63-df02cf07a0f7
  Args:
    relation: :hasFather
    source: :MariaLudwigaTheresia
    target: :LudwigIII
  AssignClass (3d7bab3c-72ab-45a5-b7af-d2980930f0f7)
 Call ID: 3d7bab3c-72ab-45a5-b7af-d2980930f0f7
  Args:
    type: :Man
    source: :CarlosOfBourbonTwoSicilies
  AssignClass (58468fcf-c177-4fe1-8ad7-38423a0c9727)
 Call ID: 58468fcf-c177-4fe1-8ad7-38423a0c9727
  Args:
    type: :Person
    source: :CarlosOfBourbonTwoSicilies
  AddTriple (969d3a1f-1bba-4191-8352-600b7a163ef0)
 Call ID: 969d3a1f-1bba-4191-8352-600b7a163ef0
  Args:
    relation: :isBrotherOf
    target: :FerdinandPius
    source: :CarlosOfBourbonTwoSicilies
  AssignClass (28597ee0-60ce-4987-bd2b-db13d92a3c66)
 Call ID: 28597ee0-60ce-4987-bd2b-db13d92a3c66
  Args:
    type: :Woman
    source: :MariaImmaculata
  AssignClass (5ac3fe35-8640-422e-bb58-7a9647a681d1)
 Call ID: 5ac3fe35-8640-422e-bb58-7a9647a681d1
  Args:
    type: :Person
    source: :MariaImmaculata
  AddTriple (f1a1b8d0-c9f6-4d1d-a233-475e7df8686e)
 Call ID: f1a1b8d0-c9f6-4d1d-a233-475e7df8686e
  Args:
    source: :MariaImmaculata
    target: :FerdinandPius
    relation: :isSisterOf
  AssignClass (ecd8622d-1933-4b9b-9a19-adf1fabe1449)
 Call ID: ecd8622d-1933-4b9b-9a19-adf1fabe1449
  Args:
    source: :MariaCristina
    type: :Woman
  AssignClass (edaba4b0-2e64-4dba-b96b-223fae1f2c83)
 Call ID: edaba4b0-2e64-4dba-b96b-223fae1f2c83
  Args:
    type: :Person
    source: :MariaCristina
  AddTriple (38aca139-9511-45b6-b482-8cd67e57043b)
 Call ID: 38aca139-9511-45b6-b482-8cd67e57043b
  Args:
    relation: :isSisterOf
    target: :FerdinandPius
    source: :MariaCristina
  AssignClass (cdc0ac6d-202f-4fde-a142-e51fb1c6a72d)
 Call ID: cdc0ac6d-202f-4fde-a142-e51fb1c6a72d
  Args:
    type: :Woman
    source: :MariaDiGrazia
  AssignClass (5dcf4bd3-2c74-48ac-bbc1-2aa7b2e60a2e)
 Call ID: 5dcf4bd3-2c74-48ac-bbc1-2aa7b2e60a2e
  Args:
    source: :MariaDiGrazia
    type: :Person
  AddTriple (43c63ba0-fb18-47a7-a229-9405197dfa73)
 Call ID: 43c63ba0-fb18-47a7-a229-9405197dfa73
  Args:
    relation: :isSisterOf
    target: :FerdinandPius
    source: :MariaDiGrazia
  AssignClass (c95cb0a3-bc26-4beb-a051-226e1a8507cc)
 Call ID: c95cb0a3-bc26-4beb-a051-226e1a8507cc
  Args:
    source: :RanieriDukeOfCastro
    type: :Man
  AssignClass (ff407483-ac24-43eb-9403-fd3757de3b6f)
 Call ID: ff407483-ac24-43eb-9403-fd3757de3b6f
  Args:
    source: :RanieriDukeOfCastro
    type: :Person
  AddTriple (f84d68a3-522b-4608-b1ff-a15a0931bed4)
 Call ID: f84d68a3-522b-4608-b1ff-a15a0931bed4
  Args:
    relation: :isBrotherOf
    target: :FerdinandPius
    source: :RanieriDukeOfCastro
  AssignClass (0a6fba00-b78a-4f12-b1a1-e24956de8072)
 Call ID: 0a6fba00-b78a-4f12-b1a1-e24956de8072
  Args:
    source: :PhilipOfBourbonTwoSicilies
    type: :Man
  AssignClass (6f93e7d1-0708-47d7-b4a7-88d926115673)
 Call ID: 6f93e7d1-0708-47d7-b4a7-88d926115673
  Args:
    type: :Person
    source: :PhilipOfBourbonTwoSicilies
  AddTriple (c8cadd4b-1c4b-42b2-b176-9c50b0c33b81)
 Call ID: c8cadd4b-1c4b-42b2-b176-9c50b0c33b81
  Args:
    target: :FerdinandPius
    source: :PhilipOfBourbonTwoSicilies
    relation: :isBrotherOf
  AssignClass (588243e3-bb4f-4418-97db-17050f287311)
 Call ID: 588243e3-bb4f-4418-97db-17050f287311
  Args:
    source: :GabrielOfBourbonTwoSicilies
    type: :Man
  AssignClass (f74ec960-1084-4a54-a6e1-30e5a14d8e43)
 Call ID: f74ec960-1084-4a54-a6e1-30e5a14d8e43
  Args:
    source: :GabrielOfBourbonTwoSicilies
    type: :Person
  AddTriple (559145ca-b8f3-4903-b018-58dfa3b6c406)
 Call ID: 559145ca-b8f3-4903-b018-58dfa3b6c406
  Args:
    relation: :isBrotherOf
    target: :FerdinandPius
    source: :GabrielOfBourbonTwoSicilies
  AssignClass (92117b64-c3f4-47c7-9ab1-2528ad823ce1)
 Call ID: 92117b64-c3f4-47c7-9ab1-2528ad823ce1
  Args:
    source: :AlfonsoDukeOfCalabria
    type: :Man
  AssignClass (9a72e6e2-20f7-4378-9f30-7c8dc6f434ae)
 Call ID: 9a72e6e2-20f7-4378-9f30-7c8dc6f434ae
  Args:
    type: :Person
    source: :AlfonsoDukeOfCalabria
  AddTriple (c5968f6a-3b1f-41fd-977f-1ae12c268b2f)
 Call ID: c5968f6a-3b1f-41fd-977f-1ae12c268b2f
  Args:
    target: :CarlosOfBourbonTwoSicilies
    source: :AlfonsoDukeOfCalabria
    relation: :hasFather
  Finish (483b1209-0276-4534-8f02-9c8e6ee922fa)
 Call ID: 483b1209-0276-4534-8f02-9c8e6ee922fa
  Args: