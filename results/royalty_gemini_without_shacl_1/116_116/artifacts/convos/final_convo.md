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
  AssignClass (988a7730-96ee-4617-bcc2-a9894210b22b)
 Call ID: 988a7730-96ee-4617-bcc2-a9894210b22b
  Args:
    type: :Man
    source: Bertrand_of_Orleans-Braganza
  AssignClass (5837b692-e42f-4c23-a851-74317e6288b9)
 Call ID: 5837b692-e42f-4c23-a851-74317e6288b9
  Args:
    type: :Person
    source: Bertrand_of_Orleans-Braganza
  AddLiteral (57e6dc10-7838-44d1-b4f3-0ef2f58a9fc1)
 Call ID: 57e6dc10-7838-44d1-b4f3-0ef2f58a9fc1
  Args:
    relation: :hasBirthYear
    literal_value: 1941
    source: Bertrand_of_Orleans-Braganza
    literal_type: xsd:integer
  AssignClass (2be13577-5d07-42f7-931b-636a661ccff4)
 Call ID: 2be13577-5d07-42f7-931b-636a661ccff4
  Args:
    type: :Man
    source: Luiz_of_Orleans-Braganza
  AssignClass (9047e702-50d6-4781-8ae6-f6dbda6b69ce)
 Call ID: 9047e702-50d6-4781-8ae6-f6dbda6b69ce
  Args:
    type: :Person
    source: Luiz_of_Orleans-Braganza
  AddTriple (3e84db4b-eb80-40c9-9948-746181c03b7a)
 Call ID: 3e84db4b-eb80-40c9-9948-746181c03b7a
  Args:
    source: Bertrand_of_Orleans-Braganza
    target: Luiz_of_Orleans-Braganza
    relation: :isBrotherOf
  AssignClass (7353b46f-063a-48f4-9fa2-e1547613d086)
 Call ID: 7353b46f-063a-48f4-9fa2-e1547613d086
  Args:
    type: :Man
    source: Pedro_Carlos
  AssignClass (285485e6-79e6-4828-9b39-9aa4407e5ed2)
 Call ID: 285485e6-79e6-4828-9b39-9aa4407e5ed2
  Args:
    type: :Person
    source: Pedro_Carlos
  AssignClass (5f365fad-2e76-4104-9196-140ea9fd8792)
 Call ID: 5f365fad-2e76-4104-9196-140ea9fd8792
  Args:
    type: :Woman
    source: Isabel_Princess_Imperial_of_Brazil
  AssignClass (ce4e3ec2-7fb2-4673-998a-2cd8a0b3eaa6)
 Call ID: ce4e3ec2-7fb2-4673-998a-2cd8a0b3eaa6
  Args:
    type: :Person
    source: Isabel_Princess_Imperial_of_Brazil
  AssignClass (f41388dc-08b3-4508-971b-23d43af43771)
 Call ID: f41388dc-08b3-4508-971b-23d43af43771
  Args:
    type: :Man
    source: Emperor_Pedro_II
  AssignClass (69285a4a-d561-4390-9230-651d6a5b8b72)
 Call ID: 69285a4a-d561-4390-9230-651d6a5b8b72
  Args:
    type: :Person
    source: Emperor_Pedro_II
  AddTriple (c2e2c50c-0a79-4888-9c75-7ae7d3c5fe33)
 Call ID: c2e2c50c-0a79-4888-9c75-7ae7d3c5fe33
  Args:
    target: Emperor_Pedro_II
    source: Isabel_Princess_Imperial_of_Brazil
    relation: :isDaughterOf
  AddTriple (afa22e8e-1208-4c3c-9db8-a754e2ed7b49)
 Call ID: afa22e8e-1208-4c3c-9db8-a754e2ed7b49
  Args:
    target: Bertrand_of_Orleans-Braganza
    source: Isabel_Princess_Imperial_of_Brazil
    relation: :isAncestorOf
  AddTriple (92c5626f-6347-46bb-a013-221d3cb121bf)
 Call ID: 92c5626f-6347-46bb-a013-221d3cb121bf
  Args:
    relation: :isAncestorOf
    source: Isabel_Princess_Imperial_of_Brazil
    target: Pedro_Carlos
  AssignClass (dd621d46-f946-4309-9dbc-14ca2a6d3e86)
 Call ID: dd621d46-f946-4309-9dbc-14ca2a6d3e86
  Args:
    type: :Man
    source: Pedro_Henrique_of_Orleans-Braganza
  AssignClass (6391c975-c001-4e33-8551-7931cc8f06f7)
 Call ID: 6391c975-c001-4e33-8551-7931cc8f06f7
  Args:
    type: :Person
    source: Pedro_Henrique_of_Orleans-Braganza
  AssignClass (9fef9ac5-63a2-48a5-88f8-fa7e7ee54e22)
 Call ID: 9fef9ac5-63a2-48a5-88f8-fa7e7ee54e22
  Args:
    type: :Woman
    source: Princess_Maria_Elisabeth_of_Bavaria
  AssignClass (d75aa723-356f-492e-ab1c-393616309079)
 Call ID: d75aa723-356f-492e-ab1c-393616309079
  Args:
    type: :Person
    source: Princess_Maria_Elisabeth_of_Bavaria
  AddTriple (15e2a242-bc8a-4755-8fc5-b98c8bf903f7)
 Call ID: 15e2a242-bc8a-4755-8fc5-b98c8bf903f7
  Args:
    relation: :isFatherOf
    source: Pedro_Henrique_of_Orleans-Braganza
    target: Bertrand_of_Orleans-Braganza
  AddTriple (3ffdbcbf-252a-4ef8-acc9-fde6fdd15756)
 Call ID: 3ffdbcbf-252a-4ef8-acc9-fde6fdd15756
  Args:
    target: Bertrand_of_Orleans-Braganza
    source: Princess_Maria_Elisabeth_of_Bavaria
    relation: :isMotherOf
  AssignClass (3c4a3adf-5bea-4339-913e-eb0239a56dff)
 Call ID: 3c4a3adf-5bea-4339-913e-eb0239a56dff
  Args:
    type: :Man
    source: Eudes_of_Orleans-Braganza
  AssignClass (9e48df1d-eb43-4ac1-a640-fd0d84f520c8)
 Call ID: 9e48df1d-eb43-4ac1-a640-fd0d84f520c8
  Args:
    type: :Person
    source: Eudes_of_Orleans-Braganza
  AddTriple (1a435382-8687-4477-9165-4ed07e5a28a2)
 Call ID: 1a435382-8687-4477-9165-4ed07e5a28a2
  Args:
    relation: :isBrotherOf
    source: Bertrand_of_Orleans-Braganza
    target: Eudes_of_Orleans-Braganza
  AssignClass (775a6752-f084-4208-b480-c700fe8e7461)
 Call ID: 775a6752-f084-4208-b480-c700fe8e7461
  Args:
    type: :Man
    source: King_Ludwig_III_of_Bavaria
  AssignClass (62355beb-343a-4d7d-9ae7-39d6730fa756)
 Call ID: 62355beb-343a-4d7d-9ae7-39d6730fa756
  Args:
    type: :Person
    source: King_Ludwig_III_of_Bavaria
  AddTriple (0e228194-0117-49b0-84d9-4a248a95687e)
 Call ID: 0e228194-0117-49b0-84d9-4a248a95687e
  Args:
    relation: :isAncestorOf
    source: King_Ludwig_III_of_Bavaria
    target: Bertrand_of_Orleans-Braganza
  Finish (e7175daf-ea51-4181-9ad6-086a8c40d58e)
 Call ID: e7175daf-ea51-4181-9ad6-086a8c40d58e
  Args: