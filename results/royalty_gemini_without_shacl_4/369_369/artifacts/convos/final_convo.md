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
Margaret of Prussia (German: Margarethe Beatrice Feodora; 22 April 1872 – 22 January 1954) was the youngest child of Frederick III, German Emperor, and Victoria, Princess Royal.
She was also the younger sister of Emperor Wilhelm II and the granddaughter of Queen Victoria.
She married Prince Frederick Charles of Hesse, the elected King of Finland, making her the would-be Queen of Finland had he not decided to renounce the throne on 14 December 1918.
In 1926, they assumed the titles of Landgrave and Landgravine of Hesse.
Early life

Princess Margaret of Prussia was the youngest of eight children born to Frederick III, then Crown Prince of the German Empire, and Victoria, Princess Royal, Britain's Queen Victoria's eldest daughter.
Born on 22 April 1872 in the Hohenzollerns' New Palace in Potsdam, by the time the infant was christened, her head was covered with short hair like moss, from which she acquired her nickname "Mossy".
Crown Princess Margherita of Italy was her godmother and Emperor Pedro II of Brazil was her godfather.
Princess Margaret grew up amid great privilege and formality.
Together with her sisters, Princess Viktoria and Princess Sophie, Margaret was deeply attached to her parents, forming an antagonist group to that of her eldest siblings, William II, Princess Charlotte and Prince Henry.
Margaret was widely regarded as the most popular of Kaiser Wilhelm II's sisters, and she maintained good relations with a wide array of family members.
She was the first cousin of both King George V of the United Kingdom and Empress Alexandra of Russia, all three being grandchildren of Victoria.
As an adult, she was said to resemble her aunt, Princess Alice.
Marriage

Princess Margaret was first attracted to Prince Maximilian of Baden.
When he did not reciprocate her affection, she moved on to her second choice, Max's close friend, Prince Frederick Charles of Hesse, future head of the Hesse-Kassel dynasty and future elected King of Finland.
At the time of the wedding, Prince Frederick Charles was not the Head of the House of Hesse-Kassel.
Prince Frederick Charles, as was his title when he married, was addressed as His Highness, while Princess Margaret warranted Royal Highness.
This disparity came to an end in 1925 when Frederick Charles became Landgrave of Hesse and Head of the house of Hesse-Kassel.
They were second cousins, both great-grandchildren of King Friedrich Wilhelm III of Prussia, he through his mother Anna, she through her father Friedrich.
Initially, her brother Wilhelm opposed the match as he felt that Frederick Charles's position was too "minor" for the Kaiser's sister.
Later, however, he gave his blessing, since Margaret herself "was so unimportant".
Princess Margaret had a strong personality; she always seemed more secure and grounded than her husband.
Margaret's husband was her mother's favorite son-in-law.
In 1901, Princess Margaret inherited Schloss Friedrichshof at the death of her mother.
However, Margaret was committed to maintain the house of her mother which entailed a great expense and the family moved to Friedrichshof.
In 1918, Margaret's husband accepted the offer of the throne of newly independent Finland, but due to German misfortunes in World War I, soon renounced it.
Family tragedies

Margaret's elder sons, Friedrich Wilhelm and Maximilian, were killed in action during World War I. Prince Maximilian, Princess Margaret's second and favorite son, was serving near Aisne when he was seriously wounded by machine gun fire in October 1914.
Princess Margaret's oldest son, Friedrich Wilhelm, died on 12 September 1916 at Kara Orman in Romania.
Her two other sons, Philipp and Christoph, embraced Nazism, and Margaret, who was the sister of the last Kaiser Wilhelm II, invited Adolf Hitler to tea and flew the swastika from her home at Schloss Kronberg.
Philipp married Princess Mafalda, daughter of King Victor Emmanuel III of Italy.
Margaret's fifth son, Christoph, was a staunch supporter of the German war effort, but after the Battle of Stalingrad, he became frustrated by the limitations placed on his own role in the conflict, and increasingly critical of the German leadership.
He was married to Princess Sophie of Greece, sister of Philip, Prince of Greece and Denmark who, in 1947, married the heir to the throne of the United Kingdom and, in 1952, became Prince Philip, Duke of Edinburgh, consort of Queen Elizabeth II.
Margaret also lost another one of her daughters-in-law during the war.
Wolfgang's wife, Princess Marie Alexandra, when she and seven other women war aid workers, were killed in a bomb attack on Frankfurt on 29–30 January 1944.
Margaret, very much the matriarch, was at the centre of her large and dynamic family.
Last years

Landgravine Margaret had difficult years after 1945; they were compounded by the theft from Schloss Friedrichshof in November 1945 of the family jewellery, valued at over £2,000,000.
Princess Margaret's son Wolfgang, fearing for the jewels, had buried them in a sub-cellar of the castle.
In early 1946, Princess Margaret discovered the theft when the family wanted to use the jewels for the wedding of Princess Sophia who was preparing to remarry.
Princess Sophia and Landgravine Margaret reported it to the Frankfurt authorities, and the culprits were imprisoned in August 1951.
The Hesse family received what had been recovered: only 10 percent of what had been stolen.
Landgravine Margaret, the last surviving child of Emperor Frederick III and last grandchild of emperor Emperor Wilhelm I, died in Kronberg on 22 January 1954, 14 years after her husband and exactly 53 years to the day after her British grandmother Queen Victoria.
Children

Landgravine Margaret and her husband Frederick Charles of Hesse had six sons, including two sets of twins:


Archives

Margaret's personal papers (including family correspondence) are preserved in the Archive of the House of Hesse, which is kept in Fasanerie Palace in Eichenzell, Germany.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (ef183f82-f85f-4531-ad22-77f647dc7101)
 Call ID: ef183f82-f85f-4531-ad22-77f647dc7101
  Args:
    type: :Woman
    source: Margaret_of_Prussia
  AssignClass (5bfcf102-05ef-4f8c-92a5-0bb6555b1307)
 Call ID: 5bfcf102-05ef-4f8c-92a5-0bb6555b1307
  Args:
    type: :Man
    source: Frederick_III_German_Emperor
  AssignClass (12b723e6-d6ba-48b3-85ce-c93f5d25d599)
 Call ID: 12b723e6-d6ba-48b3-85ce-c93f5d25d599
  Args:
    type: :Woman
    source: Victoria_Princess_Royal
  AddLiteral (2767806a-7f4a-4a8b-85c0-1abaf0ba646d)
 Call ID: 2767806a-7f4a-4a8b-85c0-1abaf0ba646d
  Args:
    literal_value: 1872
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Margaret_of_Prussia
  AddLiteral (207f8132-c7c5-439e-9c61-fe10a94d1856)
 Call ID: 207f8132-c7c5-439e-9c61-fe10a94d1856
  Args:
    literal_value: 1954
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Margaret_of_Prussia
  AddTriple (7af0c100-80f7-4deb-bee9-3a387e8e1b60)
 Call ID: 7af0c100-80f7-4deb-bee9-3a387e8e1b60
  Args:
    target: Frederick_III_German_Emperor
    relation: :hasFather
    source: Margaret_of_Prussia
  AddTriple (e7d69c6b-2ab8-41ab-9db3-ba23a218f54c)
 Call ID: e7d69c6b-2ab8-41ab-9db3-ba23a218f54c
  Args:
    relation: :hasMother
    source: Margaret_of_Prussia
    target: Victoria_Princess_Royal
  AssignClass (7a614ff9-5e3b-445d-91ea-1dfbc1619f9b)
 Call ID: 7a614ff9-5e3b-445d-91ea-1dfbc1619f9b
  Args:
    type: :Man
    source: Wilhelm_II_German_Emperor
  AddTriple (90cdd4f6-f2df-4025-bc18-f4ee9e7a2d18)
 Call ID: 90cdd4f6-f2df-4025-bc18-f4ee9e7a2d18
  Args:
    relation: :isSisterOf
    source: Margaret_of_Prussia
    target: Wilhelm_II_German_Emperor
  AssignClass (83542db9-a877-443b-9d7a-b5a1a00fccef)
 Call ID: 83542db9-a877-443b-9d7a-b5a1a00fccef
  Args:
    type: :Man
    source: Prince_Frederick_Charles_of_Hesse
  AddTriple (d7320c70-57b2-41d6-9e1d-14e7094d7b53)
 Call ID: d7320c70-57b2-41d6-9e1d-14e7094d7b53
  Args:
    target: Prince_Frederick_Charles_of_Hesse
    source: Margaret_of_Prussia
    relation: :hasRelation
  AssignClass (f9bd721e-b372-4101-a41a-1b3ba96ac75b)
 Call ID: f9bd721e-b372-4101-a41a-1b3ba96ac75b
  Args:
    type: :Woman
    source: Queen_Victoria
  AddTriple (87a5a322-4a3f-4474-800d-a75914847ab6)
 Call ID: 87a5a322-4a3f-4474-800d-a75914847ab6
  Args:
    target: Queen_Victoria
    relation: :hasAncestor
    source: Margaret_of_Prussia
  AssignClass (fb4823bf-3b2c-4964-819e-2d34e0e939f8)
 Call ID: fb4823bf-3b2c-4964-819e-2d34e0e939f8
  Args:
    type: :Woman
    source: Princess_Viktoria
  AssignClass (89acb6e0-975f-466d-a811-a8e62a5d33f2)
 Call ID: 89acb6e0-975f-466d-a811-a8e62a5d33f2
  Args:
    type: :Woman
    source: Princess_Sophie
  AddTriple (733e5017-41c8-4f62-97b3-5b91a24a6ce4)
 Call ID: 733e5017-41c8-4f62-97b3-5b91a24a6ce4
  Args:
    target: Princess_Viktoria
    source: Margaret_of_Prussia
    relation: :isSisterOf
  AddTriple (402b5526-4395-447b-8ffb-7649bdedeb4b)
 Call ID: 402b5526-4395-447b-8ffb-7649bdedeb4b
  Args:
    target: Princess_Sophie
    relation: :isSisterOf
    source: Margaret_of_Prussia
  AssignClass (99b488f3-cabf-474e-94ea-fdf8ce53fd12)
 Call ID: 99b488f3-cabf-474e-94ea-fdf8ce53fd12
  Args:
    type: :Woman
    source: Princess_Charlotte
  AssignClass (2fc9999a-681e-442a-b05d-cc5a29a3c01f)
 Call ID: 2fc9999a-681e-442a-b05d-cc5a29a3c01f
  Args:
    type: :Man
    source: Prince_Henry
  AddTriple (600e412c-5d5f-456d-b332-4b70c42e45bc)
 Call ID: 600e412c-5d5f-456d-b332-4b70c42e45bc
  Args:
    source: Margaret_of_Prussia
    relation: :isSisterOf
    target: Princess_Charlotte
  AddTriple (4bd5dd44-83cf-4097-a200-dc00a946cd9e)
 Call ID: 4bd5dd44-83cf-4097-a200-dc00a946cd9e
  Args:
    relation: :isBrotherOf
    source: Margaret_of_Prussia
    target: Prince_Henry
  AssignClass (7e765f78-54dd-4912-9cf8-30206d4ab828)
 Call ID: 7e765f78-54dd-4912-9cf8-30206d4ab828
  Args:
    type: :Man
    source: Friedrich_Wilhelm_son_of_Margaret
  AssignClass (0c43519e-9f21-4cf6-ae2f-f3cb6965e171)
 Call ID: 0c43519e-9f21-4cf6-ae2f-f3cb6965e171
  Args:
    type: :Man
    source: Maximilian_son_of_Margaret
  AssignClass (e4ba6f4b-a7e8-4c0d-acde-d943afe56eb0)
 Call ID: e4ba6f4b-a7e8-4c0d-acde-d943afe56eb0
  Args:
    type: :Man
    source: Philipp_son_of_Margaret
  AssignClass (9e43b4ef-55c8-4c49-8c87-84fd89cb881c)
 Call ID: 9e43b4ef-55c8-4c49-8c87-84fd89cb881c
  Args:
    type: :Man
    source: Christoph_son_of_Margaret
  AssignClass (22871167-11d0-4bfc-bfa6-e90296b54eb0)
 Call ID: 22871167-11d0-4bfc-bfa6-e90296b54eb0
  Args:
    type: :Man
    source: Wolfgang_son_of_Margaret
  AddTriple (81eca969-0955-482e-85bc-f575820ff6f8)
 Call ID: 81eca969-0955-482e-85bc-f575820ff6f8
  Args:
    target: Margaret_of_Prussia
    source: Friedrich_Wilhelm_son_of_Margaret
    relation: :hasMother
  AddTriple (ce2ee448-4d94-45ef-9ff6-8c229674bfe5)
 Call ID: ce2ee448-4d94-45ef-9ff6-8c229674bfe5
  Args:
    target: Margaret_of_Prussia
    relation: :hasMother
    source: Maximilian_son_of_Margaret
  AddTriple (54b628dd-c681-4468-94d2-ff474f8ae04a)
 Call ID: 54b628dd-c681-4468-94d2-ff474f8ae04a
  Args:
    target: Margaret_of_Prussia
    relation: :hasMother
    source: Philipp_son_of_Margaret
  AddTriple (8f7e0592-060d-49ba-9475-88d2bc6d6817)
 Call ID: 8f7e0592-060d-49ba-9475-88d2bc6d6817
  Args:
    relation: :hasMother
    source: Christoph_son_of_Margaret
    target: Margaret_of_Prussia
  AddTriple (d367e4aa-3a28-4f81-b44f-ad960c51aaf1)
 Call ID: d367e4aa-3a28-4f81-b44f-ad960c51aaf1
  Args:
    target: Margaret_of_Prussia
    relation: :hasMother
    source: Wolfgang_son_of_Margaret
  AddTriple (7df087d9-775b-476c-a64a-85c98c928d11)
 Call ID: 7df087d9-775b-476c-a64a-85c98c928d11
  Args:
    target: Prince_Frederick_Charles_of_Hesse
    relation: :hasFather
    source: Friedrich_Wilhelm_son_of_Margaret
  AddTriple (bf92851f-69c0-490c-a924-5048e48718d9)
 Call ID: bf92851f-69c0-490c-a924-5048e48718d9
  Args:
    target: Prince_Frederick_Charles_of_Hesse
    relation: :hasFather
    source: Maximilian_son_of_Margaret
  AddTriple (3410570d-d6c5-4637-a25b-309078ff1d3b)
 Call ID: 3410570d-d6c5-4637-a25b-309078ff1d3b
  Args:
    source: Philipp_son_of_Margaret
    relation: :hasFather
    target: Prince_Frederick_Charles_of_Hesse
  AddTriple (62b864ce-bf63-4774-9cd6-231666236efb)
 Call ID: 62b864ce-bf63-4774-9cd6-231666236efb
  Args:
    relation: :hasFather
    source: Christoph_son_of_Margaret
    target: Prince_Frederick_Charles_of_Hesse
  AddTriple (9a2e542e-0d95-446e-a41d-d6976e35a051)
 Call ID: 9a2e542e-0d95-446e-a41d-d6976e35a051
  Args:
    target: Prince_Frederick_Charles_of_Hesse
    relation: :hasFather
    source: Wolfgang_son_of_Margaret
  Finish (a5fcec5e-b2d7-4e53-a72d-97527851a806)
 Call ID: a5fcec5e-b2d7-4e53-a72d-97527851a806
  Args: