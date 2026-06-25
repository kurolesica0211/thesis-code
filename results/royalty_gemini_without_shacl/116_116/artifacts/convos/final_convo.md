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
Bertrand of Orléans-Braganza (born 2 February 1941) is the current head of the Vassouras branch of the House of Orléans-Braganza and one of the two principal claimants to the defunct Brazilian throne.
He assumed the position on 15 July 2022, following the death of his elder brother, Luiz of Orléans-Braganza.
The Vassouras branch asserts its claim in opposition to the Petrópolis branch of the Orléans-Braganzas, headed by Pedro Carlos.
Both Bertrand and Pedro Carlos are great-grandsons of Isabel, Princess Imperial of Brazil, daughter and heir of Emperor Pedro II, of the House of Braganza.
Born in Mandelieu-la-Napoule, France, the third child of Pedro Henrique of Orléans-Braganza, and Princess Maria Elisabeth of Bavaria.
Prince Bertrand is an avid traditionalist conservative, anticommunist, and outspoken advocate of right-wing Christian policies.
Although Prince Bertrand and Prince Pedro Carlos are great-grandsons of Emperor Pedro II of Brazil, of the House of Braganza, they disputed the leadership of the Brazilian Imperial Family due to a dynastic dispute regarding their parents, who were cousins.
A member of the Brazilian Imperial House, Prince Bertrand is closely related to the House of Braganza and the House of Orléans (Orleanist claimants), both through his paternal lineage, and with the House of Wittelsbach, through his maternal lineage.
He is the great-grandson of Isabel, Princess Imperial of Brazil and King Ludwig III of Bavaria.
Biography

Early life

The third son of Pedro Henrique of Orléans-Braganza and Princess Maria Elisabeth of Bavaria, his elder brothers are, in order, Luiz of Orléans-Braganza who claimed to be Head of the Brazilian Imperial Family until 2022 and Eudes of Orléans-Braganza, who renounced his dynastic rights to the Brazilian throne in order to marry a commoner.
As with his two elder brothers, Bertrand was born in southern France, 1941, even though the exile imposed on the family had already been revoked, in 1920, due to the Second World War.
Later his family moved to Paraná, where his father bought a farm and Bertrand spent his childhood.
Bertrand is a Traditionalist Catholic and a member of Tradition, Family and Property, of traditionalist Catholic inspiration, founded and directed by the intellectual leader Plinio Corrêa de Oliveira until his death.
Besides Portuguese, his native language, Bertrand is fluent in French and Spanish.
Roles

In recent years, Bertrand is coordinator and spokesman of the movement Paz no Campo (Peace in the fields), and has traveled all over Brazil lecturing for farmers and entrepreneurs in defense of private property and free enterprise.
As the activist and spokesman of the Brazilian Imperial House for the restoration of the monarchy, Bertrand has gained prominence in the national media and, on some occasions, international media, with the rise and spread of monarchist movements throughout the country.
On 22 September 2017 Bertrand participated in the program The Noite com Danilo Gentili, currently the largest talk show in the country, breaking the program's record of audience.
Political opinions

Bertrand supports typically Traditionalist Catholic ideas: he opposes same-sex marriage, favours the illegality of abortion and is against the demarcation of indigenous territory in Brazil.
Honours

As Head of the Brazilian Imperial Family, Bertrand claims the following positions:


Bertrand has also received other honours:


Ancestry

References

External links



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
  AssignClass (e08e4005-87c1-4998-9af2-bfefb31e7415)
 Call ID: e08e4005-87c1-4998-9af2-bfefb31e7415
  Args:
    type: :Man
    source: :Bertrand_of_Orléans-Braganza
  AssignClass (06f77b8c-8250-45c7-81fd-7c27dd9ee064)
 Call ID: 06f77b8c-8250-45c7-81fd-7c27dd9ee064
  Args:
    source: :Bertrand_of_Orléans-Braganza
    type: :Person
  AddLiteral (5f41c454-1ae3-43ec-a5ea-df7d1b97de5e)
 Call ID: 5f41c454-1ae3-43ec-a5ea-df7d1b97de5e
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1941
    source: :Bertrand_of_Orléans-Braganza
  AssignClass (68220c8d-bfea-4f7d-8608-e552e38f2d7a)
 Call ID: 68220c8d-bfea-4f7d-8608-e552e38f2d7a
  Args:
    type: :Man
    source: :Luiz_of_Orléans-Braganza
  AssignClass (4f8efeb2-c324-452c-bc77-c0ce1d421114)
 Call ID: 4f8efeb2-c324-452c-bc77-c0ce1d421114
  Args:
    type: :Person
    source: :Luiz_of_Orléans-Braganza
  AddTriple (f277adcf-7dfe-45e4-94f1-b7fdccf647f8)
 Call ID: f277adcf-7dfe-45e4-94f1-b7fdccf647f8
  Args:
    target: :Luiz_of_Orléans-Braganza
    source: :Bertrand_of_Orléans-Braganza
    relation: :isBrotherOf
  AssignClass (1c53fd38-927a-4a36-9d10-91ba1ef2fa46)
 Call ID: 1c53fd38-927a-4a36-9d10-91ba1ef2fa46
  Args:
    source: :Pedro_Carlos
    type: :Man
  AssignClass (1db337b2-2bb8-45dc-b6bf-70afcd00356b)
 Call ID: 1db337b2-2bb8-45dc-b6bf-70afcd00356b
  Args:
    source: :Pedro_Carlos
    type: :Person
  AssignClass (82d39bad-effe-4ae6-b544-3c95813a44e6)
 Call ID: 82d39bad-effe-4ae6-b544-3c95813a44e6
  Args:
    type: :Woman
    source: :Isabel_Princess_Imperial_of_Brazil
  AssignClass (aee33dfb-a893-413b-adf8-725896237cd6)
 Call ID: aee33dfb-a893-413b-adf8-725896237cd6
  Args:
    type: :Person
    source: :Isabel_Princess_Imperial_of_Brazil
  AssignClass (335a8cfd-673a-4f58-a865-b0bd0de46946)
 Call ID: 335a8cfd-673a-4f58-a865-b0bd0de46946
  Args:
    source: :Emperor_Pedro_II
    type: :Man
  AssignClass (d5b36485-293a-41b5-9a9e-4f5b0fcfbf94)
 Call ID: d5b36485-293a-41b5-9a9e-4f5b0fcfbf94
  Args:
    type: :Person
    source: :Emperor_Pedro_II
  AddTriple (6e613910-05c6-456a-a73c-73ee57b38459)
 Call ID: 6e613910-05c6-456a-a73c-73ee57b38459
  Args:
    relation: :isDaughterOf
    source: :Isabel_Princess_Imperial_of_Brazil
    target: :Emperor_Pedro_II
  AssignClass (300ca0a9-f819-4281-945d-9d4c4f08ca7e)
 Call ID: 300ca0a9-f819-4281-945d-9d4c4f08ca7e
  Args:
    source: :Pedro_Henrique_of_Orléans-Braganza
    type: :Man
  AssignClass (e37c1d97-984e-41b8-816b-999d1037b351)
 Call ID: e37c1d97-984e-41b8-816b-999d1037b351
  Args:
    type: :Person
    source: :Pedro_Henrique_of_Orléans-Braganza
  AssignClass (384e1b27-7092-4329-8ae9-cd1bff1bcbbb)
 Call ID: 384e1b27-7092-4329-8ae9-cd1bff1bcbbb
  Args:
    type: :Woman
    source: :Princess_Maria_Elisabeth_of_Bavaria
  AssignClass (4e8465bb-ff08-471a-a9b9-696a5dc617cc)
 Call ID: 4e8465bb-ff08-471a-a9b9-696a5dc617cc
  Args:
    source: :Princess_Maria_Elisabeth_of_Bavaria
    type: :Person
  AddTriple (a8caf0a1-b7ae-418b-9d1f-2b3d6b9f179e)
 Call ID: a8caf0a1-b7ae-418b-9d1f-2b3d6b9f179e
  Args:
    relation: :hasFather
    target: :Pedro_Henrique_of_Orléans-Braganza
    source: :Bertrand_of_Orléans-Braganza
  AddTriple (0f02634a-00aa-4772-8bd3-a5adf60811e1)
 Call ID: 0f02634a-00aa-4772-8bd3-a5adf60811e1
  Args:
    target: :Princess_Maria_Elisabeth_of_Bavaria
    source: :Bertrand_of_Orléans-Braganza
    relation: :hasMother
  AssignClass (e43af52f-ca4c-41ba-a16c-a5f2a3f96a1e)
 Call ID: e43af52f-ca4c-41ba-a16c-a5f2a3f96a1e
  Args:
    type: :Man
    source: :Eudes_of_Orléans-Braganza
  AssignClass (d6e1bde4-dd04-49f9-8927-ef4abc031847)
 Call ID: d6e1bde4-dd04-49f9-8927-ef4abc031847
  Args:
    type: :Person
    source: :Eudes_of_Orléans-Braganza
  AddTriple (5ab53ea0-8d34-4c0f-9476-1fe4813c1d12)
 Call ID: 5ab53ea0-8d34-4c0f-9476-1fe4813c1d12
  Args:
    target: :Eudes_of_Orléans-Braganza
    source: :Bertrand_of_Orléans-Braganza
    relation: :isBrotherOf
  AssignClass (3f774897-b438-44c2-9edb-92886d84a1f8)
 Call ID: 3f774897-b438-44c2-9edb-92886d84a1f8
  Args:
    type: :Man
    source: :King_Ludwig_III_of_Bavaria
  AssignClass (b8cda754-8b3e-48a4-b592-ebb8f1873bfa)
 Call ID: b8cda754-8b3e-48a4-b592-ebb8f1873bfa
  Args:
    source: :King_Ludwig_III_of_Bavaria
    type: :Person
  Finish (b4b8b6f2-fbb6-4175-bb15-eac2aa366028)
 Call ID: b4b8b6f2-fbb6-4175-bb15-eac2aa366028
  Args: