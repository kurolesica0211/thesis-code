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
Prince Philippe, Duke of Orléans (French: Louis Philippe Robert; 6 February 1869 – 28 March 1926) was the Orléanist pretender to the throne of France from 1894 to 1926 as Philippe VIII.
Early life

Philippe was born at York House, Twickenham, near London, the son of Philippe, Count of Paris, by his wife (and first cousin), Princess Isabelle of Orléans.
He was baptised with the names Louis-Philippe-Robert, and was called Philippe.
His family lived in the United Kingdom from the abdication and banishment of his great-grandfather Louis Philippe I, King of the French, in 1848, and returned to France in 1871 following the fall of the Second French Empire.
However, they again took refuge in England in 1886, when the French Republic exiled them following the wedding in Paris of Philippe's sister Amélie of Orléans to Crown Prince Carlos of Portugal.
Returning therefore to France in 1871 with his parents, Philippe was educated at home at the Château d'Eu and at the Collège Stanislas de Paris.
In 1880 Philippe's father granted him the title Duc d'Orléans.
Military career

Philippe began his military education at the École spéciale militaire de Saint-Cyr.
In October 1889, Philippe went to Switzerland to complete a course in military theory.
While there he fathered a son, Philippe Debien, by Nina, an actress working in the casino at Lausanne.
Drawn to explore the "unknown", Philippe asked Prince George, Duke of Cambridge, to send him to a military post in the Himalayas.
While in the East, he undertook a hunting and exploratory expedition in Nepal with his cousin Prince Henri of Orléans, went mountain-climbing in Tibet, and visited Afghanistan, Ceylon, and the Persian Gulf, before being posted back to Britain.
Prior to his imprisonment in France, Philippe had been unofficially engaged to his first cousin Princess Marguerite of Orléans, but the engagement was cancelled when Philippe's involvement with the Australian opera singer Nellie Melba was revealed.
Armstrong filed for divorce from Melba on the grounds of adultery, naming Philippe as co-respondent; the case was eventually dropped.
In September 1890, Philippe accompanied his father on a two-month trip to the United States and Canada.
On 12 November 1890, while in Philadelphia, Philippe joined the Pennsylvania Commandery of the Military Order of the Loyal Legion of the United States (MOLLUS) - a military society composed of officers who had served the Union in the American Civil War and their descendants - by right of his father's service in the Union Army.
In December 1890, Philippe applied unsuccessfully to serve in the Russian Army.
In March 1894, Philippe went to Egypt and Palestine with his sister Hélène, Duchess of Aosta.
Claimant to the defunct throne

Upon the death of his father on 8 September 1894, Philippe became the Orléanist claimant to the defunct French throne.
He was known to monarchists as Philippe VIII.
In October 1895, Philippe was named as co-respondent in the divorce case of Woolston v. Woolston.
Unlike his great grandfather, Louis Philippe I, Philippe claimed grand mastership of the Order of the Holy Spirit as intrinsic to his dynastic claim to the throne, and sometimes wore the breast star of the order.
On 5 November 1896, in Vienna, Philippe married Archduchess Maria Dorothea of Austria (1867–1932), a daughter of Archduke Joseph Karl of Austria, Palatine of Hungary, and granddaughter of Princess Clémentine of Orléans, as well as a niece of Marie Henriette of Austria, Queen Consort of the Belgians.
While travelling in Geneva in 1898, Philippe narrowly missed being assassinated by Luigi Lucheni, an anarchist, who vowed to kill the next member of a royal family that he saw.
He explored parts of the northeastern coast of Greenland, Denmark, in 1905 during his Duke of Orléans Arctic Expedition on ship Belgica.
Philippe continued to reside in the United Kingdom until 1912, when he moved his primary residence to Belgium.
In 1914, Philippe and his wife Maria Dorothea were legally separated.
At the outbreak of the First World War, Philippe again tried unsuccessfully to join the French army.
In 1926, Philippe died of pneumonia at the Palais d'Orléans in Palermo, Sicily, Italy.
Having no legitimate issue, he was succeeded as pretender to the defunct throne of France by his cousin and brother in law, Jean, Duke of Guise.
Publications

Philippe wrote a number of works based on his many travels: 


He also published a collection of the papers of his father and of the Henri, comte de Chambord:
Honours

In popular culture

Duke Philippe of Orleans briefly appears in an urban fantasy novel for children, The Master Key (1901) by L. Frank Baum.



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
  AssignClass (8f342f39-326f-4d5f-8ab7-feeecd3465ad)
 Call ID: 8f342f39-326f-4d5f-8ab7-feeecd3465ad
  Args:
    type: :Man
    source: Prince_Philippe_Duke_of_Orleans
  AssignClass (7d3d5395-7ee0-4806-8904-e71b307b50eb)
 Call ID: 7d3d5395-7ee0-4806-8904-e71b307b50eb
  Args:
    type: :Person
    source: Prince_Philippe_Duke_of_Orleans
  AddLiteral (eb1bfaeb-bc42-4db8-b90b-1385252cefe3)
 Call ID: eb1bfaeb-bc42-4db8-b90b-1385252cefe3
  Args:
    source: Prince_Philippe_Duke_of_Orleans
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1869
  AddLiteral (6b1dbb66-b351-4011-bd61-6af1148f0737)
 Call ID: 6b1dbb66-b351-4011-bd61-6af1148f0737
  Args:
    relation: :hasDeathYear
    literal_value: 1926
    literal_type: xsd:integer
    source: Prince_Philippe_Duke_of_Orleans
  AddLiteral (dafee280-6fd3-488e-9d08-0d6c2e5eda62)
 Call ID: dafee280-6fd3-488e-9d08-0d6c2e5eda62
  Args:
    literal_value: Louis Philippe Robert
    relation: :alsoKnownAs
    source: Prince_Philippe_Duke_of_Orleans
    literal_type: xsd:string
  AddLiteral (26ea2cdd-ad00-4aeb-b5da-4cae760ae2f3)
 Call ID: 26ea2cdd-ad00-4aeb-b5da-4cae760ae2f3
  Args:
    literal_value: Philippe VIII
    relation: :knownAs
    literal_type: xsd:string
    source: Prince_Philippe_Duke_of_Orleans
  AssignClass (e012abdb-758e-45b3-b7b2-9bf6fd02178f)
 Call ID: e012abdb-758e-45b3-b7b2-9bf6fd02178f
  Args:
    source: Philippe_Count_of_Paris
    type: :Man
  AssignClass (38134605-6d0b-4747-a4c9-1b83d24f8def)
 Call ID: 38134605-6d0b-4747-a4c9-1b83d24f8def
  Args:
    type: :Person
    source: Philippe_Count_of_Paris
  AddTriple (00b908bc-b703-4d30-93aa-71f35f11242b)
 Call ID: 00b908bc-b703-4d30-93aa-71f35f11242b
  Args:
    relation: :hasFather
    target: Philippe_Count_of_Paris
    source: Prince_Philippe_Duke_of_Orleans
  AssignClass (b4d87362-b253-4afe-91dc-77ed1b3f84cc)
 Call ID: b4d87362-b253-4afe-91dc-77ed1b3f84cc
  Args:
    source: Princess_Isabelle_of_Orleans
    type: :Woman
  AssignClass (552585ea-63bc-42ad-b3e0-a081f9d8be2f)
 Call ID: 552585ea-63bc-42ad-b3e0-a081f9d8be2f
  Args:
    source: Princess_Isabelle_of_Orleans
    type: :Person
  AddTriple (c476a6c9-0bf6-4bce-b03d-e41437e3bc87)
 Call ID: c476a6c9-0bf6-4bce-b03d-e41437e3bc87
  Args:
    relation: :hasMother
    target: Princess_Isabelle_of_Orleans
    source: Prince_Philippe_Duke_of_Orleans
  AssignClass (48c56e5b-b7fe-4b2d-961c-32f68da4a13d)
 Call ID: 48c56e5b-b7fe-4b2d-961c-32f68da4a13d
  Args:
    type: :Man
    source: Philippe_Debien
  AssignClass (13b9c152-caac-4c81-89bf-451ad25e4480)
 Call ID: 13b9c152-caac-4c81-89bf-451ad25e4480
  Args:
    type: :Person
    source: Philippe_Debien
  AddTriple (66d09ad4-7009-4724-a827-5d0493099012)
 Call ID: 66d09ad4-7009-4724-a827-5d0493099012
  Args:
    source: Philippe_Debien
    target: Prince_Philippe_Duke_of_Orleans
    relation: :isSonOf
  AssignClass (a8ae486a-f09d-4ae5-8e31-092c9bbcccf2)
 Call ID: a8ae486a-f09d-4ae5-8e31-092c9bbcccf2
  Args:
    type: :Woman
    source: Nina
  AssignClass (5f31bdff-55d6-4610-a9aa-6f842745dfe6)
 Call ID: 5f31bdff-55d6-4610-a9aa-6f842745dfe6
  Args:
    type: :Person
    source: Nina
  AddTriple (cc029908-df88-4326-976a-0472774ba1a3)
 Call ID: cc029908-df88-4326-976a-0472774ba1a3
  Args:
    target: Philippe_Debien
    relation: :isMotherOf
    source: Nina
  AssignClass (c2642985-b7ae-4fba-a3e6-a320e7523202)
 Call ID: c2642985-b7ae-4fba-a3e6-a320e7523202
  Args:
    type: :Woman
    source: Amelie_of_Orleans
  AssignClass (ee89b69b-6156-47b4-8552-8f4cbb87288a)
 Call ID: ee89b69b-6156-47b4-8552-8f4cbb87288a
  Args:
    source: Amelie_of_Orleans
    type: :Person
  AddTriple (976f6d34-ad0c-4f10-a636-1bee068926a9)
 Call ID: 976f6d34-ad0c-4f10-a636-1bee068926a9
  Args:
    source: Amelie_of_Orleans
    target: Prince_Philippe_Duke_of_Orleans
    relation: :isSisterOf
  AssignClass (6d62dd88-7bae-4fe5-a731-851612f6cefe)
 Call ID: 6d62dd88-7bae-4fe5-a731-851612f6cefe
  Args:
    source: Helene_Duchess_of_Aosta
    type: :Woman
  AssignClass (cf0f5a28-23b1-42f9-901b-87211a10382c)
 Call ID: cf0f5a28-23b1-42f9-901b-87211a10382c
  Args:
    source: Helene_Duchess_of_Aosta
    type: :Person
  AddTriple (02865f78-4348-43e6-aca9-2f762d79f68f)
 Call ID: 02865f78-4348-43e6-aca9-2f762d79f68f
  Args:
    source: Helene_Duchess_of_Aosta
    relation: :isSisterOf
    target: Prince_Philippe_Duke_of_Orleans
  AssignClass (39cce5d0-3bd8-4ab3-8814-60f2aa089479)
 Call ID: 39cce5d0-3bd8-4ab3-8814-60f2aa089479
  Args:
    type: :Woman
    source: Archduchess_Maria_Dorothea_of_Austria
  AssignClass (215e2774-a5d2-4fdd-b981-c7847d44740e)
 Call ID: 215e2774-a5d2-4fdd-b981-c7847d44740e
  Args:
    type: :Person
    source: Archduchess_Maria_Dorothea_of_Austria
  AddTriple (dd2d5e41-65c8-4be2-8d63-3ab5a02f4359)
 Call ID: dd2d5e41-65c8-4be2-8d63-3ab5a02f4359
  Args:
    target: Archduchess_Maria_Dorothea_of_Austria
    relation: :hasRelation
    source: Prince_Philippe_Duke_of_Orleans
  AddLiteral (f4e49cb9-224a-47e2-aa7c-1def67657a63)
 Call ID: f4e49cb9-224a-47e2-aa7c-1def67657a63
  Args:
    literal_type: xsd:integer
    source: Prince_Philippe_Duke_of_Orleans
    literal_value: 1896
    relation: :hasMarriageYear
  Finish (bbd1bf73-da59-40af-a4d2-f1a5d292b33e)
 Call ID: bbd1bf73-da59-40af-a4d2-f1a5d292b33e
  Args: