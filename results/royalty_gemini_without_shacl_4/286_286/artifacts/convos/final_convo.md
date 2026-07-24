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
Rafael of Orléans-Braganza (Portuguese: Rafael de Orléans e Bragança; born 24 April 1986) is a member of the Imperial House of Brazil.
He is the heir presumptive to his childless uncle, Prince Bertrand, the current head of the Vassouras branch of the House of Orléans-Braganza and one of the claimants to the defunct Brazilian Throne.
Rafael became heir presumptive following the death of his father, Prince Antônio, in November 2024.
Family

Born in Petrópolis, Brazil on 26 April 1986, he is the third child and second son of Prince Antônio de Orleans e Bragança and Princess Christine of Ligne.
He has an older brother and sister, Prince Pedro Luiz and Princess Amélia and a younger sister, Princess Maria Gabriela.
His name in full is Rafael Antonio Maria José Francisco Miguel Gabriel Gonzaga de Orléans e Bragança e Ligne.
His paternal grandparents were Prince Pedro Henrique of Orléans-Bragança, one of two claimants to be head of the Brazilian Imperial House, and Princess Maria Elisabeth of Bavaria.
His maternal grandparents were Antoine, 13th Prince of Ligne, and Princess Alix of Luxembourg.
His mother's family, the House of Ligne, is one of the oldest and most prominent Wallonian noble families still extant in Belgium.
Christine is a niece of Grand Duke Jean, who reigned in Luxembourg until his abdication in 2000.
Personal life

Rafael has a degree in manufacturing engineering from Pontifical Catholic University of Rio de Janeiro, working at the InBev subsidiary in London.
Rafael also has a partnership and a tourism enterprise with headquarters in New York, Paris and Rio de Janeiro.
Rafael has expressed in statements his desire to marry a princess who is part of "Catholic royalty or high nobility".
Appointments

In February 2022, after the floods that devastated the city of Petrópolis, Rafael came to the aid of the victims, bringing them essential goods that the imperial house received from monarchist supporters.
Honors

Genealogy

Ancestry

Patrilineal descent

Rafael is a member of the House of Orléans-Braganza, a sub-branch of the House of Bourbon, itself a branch of the House of Capet and of the Robertians.
Rafael's patriline is the line from which he is descended father to son.
It follows the Dukes of Orléans, the Kings of France, the Dukes and Counts of Vendôme, the Counts of La Marche, the first Duke of Bourbon, a Count of Clermont, and before them, again the Kings of France.



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
  AssignClass (787ad794-da30-4f35-bdfe-ba9d1b257539)
 Call ID: 787ad794-da30-4f35-bdfe-ba9d1b257539
  Args:
    type: :Man
    source: Rafael_of_Orléans-Braganza
  AssignClass (4f48f166-1298-4425-b16a-a068b8599a58)
 Call ID: 4f48f166-1298-4425-b16a-a068b8599a58
  Args:
    type: :Person
    source: Rafael_of_Orléans-Braganza
  AddLiteral (243654e9-a001-4d35-ab01-e56d562c79a4)
 Call ID: 243654e9-a001-4d35-ab01-e56d562c79a4
  Args:
    literal_value: 1986
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Rafael_of_Orléans-Braganza
  AssignClass (36c63830-5711-40ce-a518-d5422be51809)
 Call ID: 36c63830-5711-40ce-a518-d5422be51809
  Args:
    type: :Man
    source: Prince_Bertrand
  AssignClass (cb41b728-8ea1-43f3-a9f3-cd8ea3940cc5)
 Call ID: cb41b728-8ea1-43f3-a9f3-cd8ea3940cc5
  Args:
    type: :Person
    source: Prince_Bertrand
  AssignClass (ba13c6cd-f1c1-4c16-84ac-efa77e911800)
 Call ID: ba13c6cd-f1c1-4c16-84ac-efa77e911800
  Args:
    type: :Man
    source: Prince_Antônio
  AssignClass (3d7e2849-a7c0-486e-911a-99cde27568b9)
 Call ID: 3d7e2849-a7c0-486e-911a-99cde27568b9
  Args:
    type: :Person
    source: Prince_Antônio
  AddLiteral (50a33215-1da9-4460-96df-f47a51ded70d)
 Call ID: 50a33215-1da9-4460-96df-f47a51ded70d
  Args:
    source: Prince_Antônio
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2024
  AssignClass (4619e092-8b28-4a9e-859b-bf666c09fb8e)
 Call ID: 4619e092-8b28-4a9e-859b-bf666c09fb8e
  Args:
    type: :Woman
    source: Princess_Christine_of_Ligne
  AssignClass (746d6d8e-7740-4d34-bc93-c9ec308f79a3)
 Call ID: 746d6d8e-7740-4d34-bc93-c9ec308f79a3
  Args:
    type: :Person
    source: Princess_Christine_of_Ligne
  AddTriple (a8478f09-6cd1-46f1-915f-e336811af8d0)
 Call ID: a8478f09-6cd1-46f1-915f-e336811af8d0
  Args:
    target: Prince_Antônio
    relation: :hasFather
    source: Rafael_of_Orléans-Braganza
  AddTriple (a17965b8-3262-472f-993d-224889e370c6)
 Call ID: a17965b8-3262-472f-993d-224889e370c6
  Args:
    source: Rafael_of_Orléans-Braganza
    target: Princess_Christine_of_Ligne
    relation: :hasMother
  AssignClass (3128f3b3-0dff-4da8-bf7e-b3723d9ec6ed)
 Call ID: 3128f3b3-0dff-4da8-bf7e-b3723d9ec6ed
  Args:
    type: :Man
    source: Prince_Pedro_Luiz
  AssignClass (0748d109-48c1-4097-bab5-417016d2d2a0)
 Call ID: 0748d109-48c1-4097-bab5-417016d2d2a0
  Args:
    type: :Person
    source: Prince_Pedro_Luiz
  AssignClass (dd42cbdf-7d7d-496d-bdd2-e6b0f8bdd321)
 Call ID: dd42cbdf-7d7d-496d-bdd2-e6b0f8bdd321
  Args:
    type: :Woman
    source: Princess_Amélia
  AssignClass (55fc32be-84c4-4682-ac20-c90bf6b480aa)
 Call ID: 55fc32be-84c4-4682-ac20-c90bf6b480aa
  Args:
    type: :Person
    source: Princess_Amélia
  AssignClass (b7e5068e-88ac-4045-935c-641fff3d26e4)
 Call ID: b7e5068e-88ac-4045-935c-641fff3d26e4
  Args:
    type: :Woman
    source: Princess_Maria_Gabriela
  AssignClass (f668ef41-c890-4b4d-af73-ce2b15906a10)
 Call ID: f668ef41-c890-4b4d-af73-ce2b15906a10
  Args:
    type: :Person
    source: Princess_Maria_Gabriela
  AddTriple (6b03563a-3431-409f-9956-0cb1e0c79593)
 Call ID: 6b03563a-3431-409f-9956-0cb1e0c79593
  Args:
    source: Rafael_of_Orléans-Braganza
    relation: :isSiblingOf
    target: Prince_Pedro_Luiz
  AddTriple (647e84a8-2b6f-44c7-9257-f47156ef77cb)
 Call ID: 647e84a8-2b6f-44c7-9257-f47156ef77cb
  Args:
    target: Princess_Amélia
    relation: :isSiblingOf
    source: Rafael_of_Orléans-Braganza
  AddTriple (37bc37f1-7223-4a7a-bf24-066af4249e06)
 Call ID: 37bc37f1-7223-4a7a-bf24-066af4249e06
  Args:
    target: Princess_Maria_Gabriela
    relation: :isSiblingOf
    source: Rafael_of_Orléans-Braganza
  AssignClass (94cf74af-6dee-47d3-bd1b-af7b3fa5537d)
 Call ID: 94cf74af-6dee-47d3-bd1b-af7b3fa5537d
  Args:
    type: :Man
    source: Prince_Pedro_Henrique
  AssignClass (7a8d3da4-cb23-4460-8f08-8f69cc731777)
 Call ID: 7a8d3da4-cb23-4460-8f08-8f69cc731777
  Args:
    type: :Person
    source: Prince_Pedro_Henrique
  AssignClass (bb0658f2-a4d3-44b9-83dc-0d4a3dbd2e64)
 Call ID: bb0658f2-a4d3-44b9-83dc-0d4a3dbd2e64
  Args:
    type: :Woman
    source: Princess_Maria_Elisabeth_of_Bavaria
  AssignClass (b76119e2-6ac4-45dd-a614-ed5f323ea8d2)
 Call ID: b76119e2-6ac4-45dd-a614-ed5f323ea8d2
  Args:
    type: :Person
    source: Princess_Maria_Elisabeth_of_Bavaria
  AddTriple (2f466a14-5329-4a22-a034-2ec66e377e0d)
 Call ID: 2f466a14-5329-4a22-a034-2ec66e377e0d
  Args:
    target: Prince_Pedro_Henrique
    relation: :hasFather
    source: Prince_Antônio
  AddTriple (faaeffe0-59bb-4a3b-991a-58df0293559b)
 Call ID: faaeffe0-59bb-4a3b-991a-58df0293559b
  Args:
    source: Prince_Antônio
    target: Princess_Maria_Elisabeth_of_Bavaria
    relation: :hasMother
  AssignClass (fe67e8ed-32b8-4065-b270-37e82d2ca663)
 Call ID: fe67e8ed-32b8-4065-b270-37e82d2ca663
  Args:
    type: :Man
    source: Antoine_13th_Prince_of_Ligne
  AssignClass (6e5f5f00-3af1-4424-975c-59a2caba809e)
 Call ID: 6e5f5f00-3af1-4424-975c-59a2caba809e
  Args:
    type: :Person
    source: Antoine_13th_Prince_of_Ligne
  AssignClass (bce61a26-eef6-40d8-847f-b62cdc38674b)
 Call ID: bce61a26-eef6-40d8-847f-b62cdc38674b
  Args:
    type: :Woman
    source: Princess_Alix_of_Luxembourg
  AssignClass (39116079-01ce-4c0b-b4cc-32751089592e)
 Call ID: 39116079-01ce-4c0b-b4cc-32751089592e
  Args:
    type: :Person
    source: Princess_Alix_of_Luxembourg
  AddTriple (49306870-04d1-4fec-965c-fb63080e0204)
 Call ID: 49306870-04d1-4fec-965c-fb63080e0204
  Args:
    relation: :hasFather
    target: Antoine_13th_Prince_of_Ligne
    source: Princess_Christine_of_Ligne
  AddTriple (5cf69cec-d3f2-4184-9734-aa8f4a3c54dc)
 Call ID: 5cf69cec-d3f2-4184-9734-aa8f4a3c54dc
  Args:
    source: Princess_Christine_of_Ligne
    target: Princess_Alix_of_Luxembourg
    relation: :hasMother
  AssignClass (a6c4c281-1ccc-45b1-989a-6216b018a3d2)
 Call ID: a6c4c281-1ccc-45b1-989a-6216b018a3d2
  Args:
    type: :Man
    source: Grand_Duke_Jean
  AssignClass (acdccc96-f4ae-40c1-8ba7-98869891ce80)
 Call ID: acdccc96-f4ae-40c1-8ba7-98869891ce80
  Args:
    type: :Person
    source: Grand_Duke_Jean
  Finish (580f5fd5-0ec1-4796-b0ec-bc192f999e4c)
 Call ID: 580f5fd5-0ec1-4796-b0ec-bc192f999e4c
  Args: