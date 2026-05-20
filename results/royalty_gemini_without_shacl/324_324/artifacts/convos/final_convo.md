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
Henri d'Orléans (Henri Robert Ferdinand Marie d'Orléans; 5 July 1908 – 19 June 1999), was the Orléanist pretender to the defunct throne of France as Henry VI from 1940 until his death in 1999.
Henri was the direct descendant of Philippe I, Duke of Orléans, son of Louis XIII.
He was also a descendant of Louis XIV through a female line, from his legitimized daughter Françoise Marie de Bourbon, as well as the great-great-grandson, by four different lines of descent, of Louis Philippe I.
The son of Jean, Duke of Guise, Henri was forbidden to enter France for much of his life.
Henri worked to restore the French monarchy in a parliamentary form, and discussed the topic with Charles de Gaulle.
Upon his death in 1999, his son Henri succeeded him as Head of the House of Orléans.
Here, Henri rose at 4 am daily, accompanying his father to oversee livestock management and crop production on their scattered lands, later in the day being tutored by European governesses and his mother: He acquired fluency in French, Arabic, English, German, Italian and Spanish.
Being rebuffed by France, Belgium and the United Kingdom, Prince Jean finally took his family back to Morocco and farming.
In 1921, Henri's governesses were replaced with a series of preceptors, all coming from France.
In 1923, the abbé Thomas took over Henri's instruction and, being less traditional in his approach, awakened in his charge a hitherto undetected thirst for knowledge.
Using the wedding of the prince's sister that year in France as an opportunity, Thomas obtained permission to take Henri to the Parisian banlieues of Meudon and Issy-les-Moulineaux, then working class slums in which the abbé would volunteer to serve the needy daily, bringing Henri into close contact with day laborers.
After a year Thomas, whose health suffered in Morocco, was replaced as Henri's preceptor by abbé Dartein, who accompanied the family to France in 1924, preparing the prince for his collegiate matriculation while they occupied an apartment near his parents in Paris.
Henri began a two-year study of mathematics and the sciences at the Catholic University of Louvain in 1924, studying the law for the two years following.
From across the border in France came scholars and veterans of renown to coach Henri for his future role as a royalist leader, including jurist Ernest Perrot, military strategist Général Henri de Gondrecourt and the diplomat Charles Benoist, a member of the Académie des Sciences Morales et Politiques who would serve as his advisor from 1930.
Dauphin in pretence

In 1926, Henri became the Dauphin of France in pretence when his father became the Orléanist claimant to the defunct throne upon the death of his maternal uncle, Philippe, Duke of Orleans.
In 1939, after being refused admission to both the French and the British armed forces, Henri was allowed to join the French Foreign Legion.
Orléanist pretender

World War II

Henri became pretender to the defunct French throne on 25 August 1940 when his father died.
Henri was a "gentlemen farmer" in Morocco in the course of 1942.
In mid-November 1942, after Admiral François Darlan's armistice with the Allied invaders of North Africa, Vichy intelligence official Henri d'Astier de la Vigerie attempted to promote a royalist coup (d'Astier had previously conspired with the Allies to aid the invasion).
He proposed that Henri would appear to head a French government composed of all political tendencies, and maintain "neutrality until the day comes when the French nation can freely decide for itself."
Ridgeway was taken aback by the proposal, but was unaware that d'Astier's colleagues, Abbé Cordier and Master-Sergeant Sabatier (a French instructor at an OSS-SOE camp in Algiers), had secretly brought Henri from Morocco to d'Astier's apartment in Algiers.
Post war

In 1947, Henri and his family took up residence at the Quinta do Anjinho, an estate in Sintra, on the Portuguese Riviera.
In 1950, after the law of exile was rescinded, Henri returned to France.
During his tenure as pretender to the defunct throne, Henri used the majority of his family's great wealth, selling off family jewels, paintings, furniture and properties to support his political cause and large family, as well as establishments in Belgium, North Africa, Brazil, Portugal and France.
Political activity

Unlike his father, Henri devoted his life to politics.
During World War II, Henri was initially sympathetic to Vichy France.
Laval offered Henri the unglamorous position of Minister of Food, which he declined.
In Algeria, Henri attempted to convince the French military governor not to oppose an Anglo-American military landing.
Henri had correctly predicted such a thing occurring, but at the time he was laughed at by the officers.
Henri also tried to mediate between Charles de Gaulle and Henri Giraud, when the two men were competing for control of Free France.
Between 1940 and 1941, the Gaullist camp offered Henri an invitation to go to London, which he declined.
Henri feared that if he accepted the offer, he would have become an émigré, like the Bourbons who returned to France after Napoleon's defeat.
Henri was staunchly opposed to the idea of siding with one political party, wishing instead to pursue a path of unity and not contribute to France's "infernal divisiveness."
"


In 1948, Henri began publishing a monthly bulletin, which soon possessed 30,000 subscribers.
In 1950, the French Parliament abrogated the Law of Exile, permitting Henri to return.
So we have to make do with Henri, who strikes a royal enough pose, I guess.
In 1954, Henri met Charles de Gaulle and continued their relationship through correspondence.
In 1958, Henri gave his support to de Gaulle, who was called back from his self-imposed exile to save the French Republic from insurrection in Paris.
Thereafter, Henri became a frequent visitor to the Élysée Palace, where de Gaulle waited for Henri "by the staircase or outside, reserved a special armchair for him and lit his cigarette."
There, they frequently discussed French history together, with Henri noting that de Gaulle loved to pronounce the word 'king'.
In 1960, de Gaulle told Henri that "Monseigneur, I believe deeply in the value of the monarchy, and I am certain as well that this regime is the one best suited to our poor country."
The following year, de Gaulle dispatched Henri on a tour to Libya, Ethiopia, Iran, and Lebanon, with the purpose of explaining France's Algeria policy, serving as de Gaulle's special representative, or "pro-consul."
During this time, Henri befriended Hassan II of Morocco and Habib Bourguiba.
In 1962, de Gaulle informed Henri in strict confidence that he had arranged the French presidential election so that the head of the royal house could succeed him as president of the Republic.
However, by 1964, de Gaulle changed his mind and told Henri of his decision to run for re-election, which he won.
By 1968, Henri ceased publication of his paper over his increasing disagreements with the Gaullists.
The Countess of Paris remarked that "Under de Gaulle, Henri came two fingers close to becoming king.
"


Following de Gaulle's death in 1970, his son Philippe de Gaulle told Henri, "Monseigneur, my father often told me that if circumstances had been different, he would have been happy to be your faithful and loyal servant."
In 1979, Henri published his book Mémoires d'exil et de combats, which revealed to the public that de Gaulle had asked Henri to prepare himself for the 1965 presidential elections in France.
In a latter interview, Henri stated "At all times de Gaulle desired restoration, I am convinced of it.
However, Henri also noted that "It was difficult to get anywhere without de Gaulle, He agreed to favor my ascension to the highest point, but he didn't understand that it was necessary to give me the means of getting there.
"


Henri stated that he believes de Gaulle never forgave him for refusing to join the Free French in London, and also noted that "De Gaulle was not my friend...De Gaulle and I shared some common ideals and I agreed with him on the essentials of his approach to politics...
"


In 1988, Henri produced a scandal among his monarchist supporters when he supported the re-election of François Mitterrand, a socialist.
Political beliefs

In his college years, Henri spent many nights listening to the French monarchist writer Charles Maurras.
But during his adult life, Henri considered himself a centrist and never allied with any political party.
On Action Française, Henri stated that it had many talented leaders, but he ultimately regarded it as "a Rightist party with extreme Right sympathies."
In Henri's view, "no one should be in a position to claim a monopoly on the monarchist idea.
"


Henri befriended politicians on both the left and right, and declined to run for Parliament, despite de Gaulle's suggestion that he should do so.
Some rightist critics of Henri regarded him as "the Crown Prince of the Republic" or "a dyed-in-the-wool socialist, if not a Jacobin."
"


Henri was a critic of primogeniture and favored elective monarchy over hereditary.
Marriage and family life

On 8 April 1931, he married Princess Isabelle of Orléans-Braganza.
The wedding was celebrated in Palermo Cathedral in Sicily, the same church where their common ancestors, Louis Philippe of France and his Queen Maria Amalia, married in 1809.
In 1984, Henri declared that his son, Henri of Orléans, had lost his rights of inheritance because he had divorced his first wife and married a second time, outside of the Roman Catholic Church.
Henri gave his son the lesser-valued title comte de Mortain in place of comte de Clermont, and removed him from the line of succession.
After a couple of years, Henri reinstated his son with his previous titles, including reestablishing him as heir apparent and gave his new wife, Micaela Cousiño Quinones de Leon, the title "princesse de Joinville".
Henri deprived his sons Thibaut and Michel of their rights of succession to the defunct throne, because one married a commoner and the other wed a noblewoman whose father had been compromised during the Vichy regime.
His decision was later annulled by his son and successor, Henri.
Death

Henri, Count of Paris, died of prostate cancer at Cherisy, near Dreux, France, aged 90 on 19 June 1999.
Incidentally, his grandson Prince Eudes, Duke of Angoulême married on the very same day.
Issue

Henri, Count of Paris, and his wife Isabelle had eleven children:


Ancestry

References

Further reading

External links



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (f94029ed-39c9-4be6-af42-5e15d5dfecc6)
 Call ID: f94029ed-39c9-4be6-af42-5e15d5dfecc6
  Args:
    source: Henri_d_Orleans
    type: :Man
  AssignClass (1b799f75-2b74-4b23-8179-ca0effa2dede)
 Call ID: 1b799f75-2b74-4b23-8179-ca0effa2dede
  Args:
    type: :Person
    source: Henri_d_Orleans
  AssignClass (7b0a0eae-3e57-4ec9-896a-6a9baa7604a4)
 Call ID: 7b0a0eae-3e57-4ec9-896a-6a9baa7604a4
  Args:
    source: Henri_d_Orleans
    type: :Ancestor
  AddLiteral (47c685af-f6d6-48d8-9858-bc8b2621ab5b)
 Call ID: 47c685af-f6d6-48d8-9858-bc8b2621ab5b
  Args:
    literal_value: 1908
    source: Henri_d_Orleans
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (90b3c3aa-122e-40ba-a3b5-b83d5108bf73)
 Call ID: 90b3c3aa-122e-40ba-a3b5-b83d5108bf73
  Args:
    literal_value: 1999
    relation: :hasDeathYear
    source: Henri_d_Orleans
    literal_type: xsd:integer
  AssignClass (597413af-12f9-4b13-9d25-87bedaa2d5fc)
 Call ID: 597413af-12f9-4b13-9d25-87bedaa2d5fc
  Args:
    source: Jean_Duke_of_Guise
    type: :Man
  AssignClass (10cc0065-1340-4a4f-b492-3f4685434b43)
 Call ID: 10cc0065-1340-4a4f-b492-3f4685434b43
  Args:
    source: Jean_Duke_of_Guise
    type: :Person
  AssignClass (53f6e085-fc31-48a4-9acd-30ab0b11fdcc)
 Call ID: 53f6e085-fc31-48a4-9acd-30ab0b11fdcc
  Args:
    type: :Ancestor
    source: Jean_Duke_of_Guise
  AddTriple (3f38f298-44bb-41c9-8544-7dd5d349b663)
 Call ID: 3f38f298-44bb-41c9-8544-7dd5d349b663
  Args:
    target: Jean_Duke_of_Guise
    source: Henri_d_Orleans
    relation: :hasFather
  AssignClass (076c335e-6dbd-49fd-8349-72d894c4b100)
 Call ID: 076c335e-6dbd-49fd-8349-72d894c4b100
  Args:
    type: :Woman
    source: Isabelle_of_Orleans_Braganza
  AssignClass (283cb884-ff39-4976-b11b-cc1ea069d920)
 Call ID: 283cb884-ff39-4976-b11b-cc1ea069d920
  Args:
    type: :Person
    source: Isabelle_of_Orleans_Braganza
  AddTriple (96f077a5-f3a6-4cc3-80df-36a61f7e8e86)
 Call ID: 96f077a5-f3a6-4cc3-80df-36a61f7e8e86
  Args:
    source: Henri_d_Orleans
    relation: :hasMother
    target: Isabelle_of_Orleans_Braganza
  AddLiteral (a9243ad4-e8b1-454d-8028-a91f7ef47d33)
 Call ID: a9243ad4-e8b1-454d-8028-a91f7ef47d33
  Args:
    relation: :hasMarriageYear
    source: Henri_d_Orleans
    literal_type: xsd:integer
    literal_value: 1931
  AssignClass (fefecc0b-134a-40ee-941e-2273dc7606da)
 Call ID: fefecc0b-134a-40ee-941e-2273dc7606da
  Args:
    type: :Man
    source: Henri_of_Orleans_son
  AssignClass (1bcdd12c-53c6-4e4b-8081-146c111851a6)
 Call ID: 1bcdd12c-53c6-4e4b-8081-146c111851a6
  Args:
    source: Henri_of_Orleans_son
    type: :Person
  AssignClass (a5576d99-a7ed-4df5-aad4-668323619fea)
 Call ID: a5576d99-a7ed-4df5-aad4-668323619fea
  Args:
    type: :Ancestor
    source: Henri_of_Orleans_son
  AddTriple (068c3072-9ee5-4f4f-b42a-2453d4557822)
 Call ID: 068c3072-9ee5-4f4f-b42a-2453d4557822
  Args:
    source: Henri_of_Orleans_son
    relation: :hasFather
    target: Henri_d_Orleans
  AssignClass (bd9f8f3b-5d72-4232-967d-9d3a77431499)
 Call ID: bd9f8f3b-5d72-4232-967d-9d3a77431499
  Args:
    type: :Man
    source: Thibaut
  AssignClass (56cfa7af-2e22-4139-8068-ff361e1a1d02)
 Call ID: 56cfa7af-2e22-4139-8068-ff361e1a1d02
  Args:
    source: Thibaut
    type: :Person
  AddTriple (631ad515-6960-4c12-9365-32325115db04)
 Call ID: 631ad515-6960-4c12-9365-32325115db04
  Args:
    relation: :hasFather
    source: Thibaut
    target: Henri_d_Orleans
  AssignClass (51cd1688-f545-4341-8b0d-4710fbb2ea27)
 Call ID: 51cd1688-f545-4341-8b0d-4710fbb2ea27
  Args:
    type: :Man
    source: Michel
  AssignClass (474d77ec-94c7-4d24-ad51-94f33bdbcb13)
 Call ID: 474d77ec-94c7-4d24-ad51-94f33bdbcb13
  Args:
    source: Michel
    type: :Person
  AddTriple (44eca576-01be-44ff-9c22-7f0b9e05cb0e)
 Call ID: 44eca576-01be-44ff-9c22-7f0b9e05cb0e
  Args:
    target: Henri_d_Orleans
    source: Michel
    relation: :hasFather
  AssignClass (3c22a4be-58ee-4d2d-922d-74ed3892eb14)
 Call ID: 3c22a4be-58ee-4d2d-922d-74ed3892eb14
  Args:
    type: :Man
    source: Philippe_I_Duke_of_Orleans
  AssignClass (3c519a1c-ca0a-4d5f-9faf-5a39922afb1a)
 Call ID: 3c519a1c-ca0a-4d5f-9faf-5a39922afb1a
  Args:
    source: Philippe_I_Duke_of_Orleans
    type: :Ancestor
  AddTriple (0fce429b-2b36-477b-ac75-5c11d28ae6db)
 Call ID: 0fce429b-2b36-477b-ac75-5c11d28ae6db
  Args:
    target: Philippe_I_Duke_of_Orleans
    source: Henri_d_Orleans
    relation: :hasAncestor
  AssignClass (3761c662-fc6e-4f06-b7d1-906ded604101)
 Call ID: 3761c662-fc6e-4f06-b7d1-906ded604101
  Args:
    source: Louis_XIII
    type: :Man
  AssignClass (80de5fea-9ea9-49b6-9651-538a1bd78e25)
 Call ID: 80de5fea-9ea9-49b6-9651-538a1bd78e25
  Args:
    type: :Ancestor
    source: Louis_XIII
  AddTriple (11ef0bd4-57f9-4b22-9502-e893014c2f55)
 Call ID: 11ef0bd4-57f9-4b22-9502-e893014c2f55
  Args:
    source: Philippe_I_Duke_of_Orleans
    relation: :hasFather
    target: Louis_XIII
  AssignClass (13817edb-e538-4759-a318-590683374930)
 Call ID: 13817edb-e538-4759-a318-590683374930
  Args:
    type: :Man
    source: Louis_XIV
  AssignClass (a162f6ff-48a4-4bfc-97c0-408d7f37c9bc)
 Call ID: a162f6ff-48a4-4bfc-97c0-408d7f37c9bc
  Args:
    source: Louis_XIV
    type: :Ancestor
  AssignClass (a693b1d7-c7e0-441b-a2b4-b0b9c6413b88)
 Call ID: a693b1d7-c7e0-441b-a2b4-b0b9c6413b88
  Args:
    type: :Woman
    source: Francoise_Marie_de_Bourbon
  AssignClass (910be1e3-c6b8-4b6f-a10f-97e25fa750dd)
 Call ID: 910be1e3-c6b8-4b6f-a10f-97e25fa750dd
  Args:
    type: :Ancestor
    source: Francoise_Marie_de_Bourbon
  AddTriple (c3557ed8-1f0b-4bc8-a131-f71dce048d89)
 Call ID: c3557ed8-1f0b-4bc8-a131-f71dce048d89
  Args:
    source: Francoise_Marie_de_Bourbon
    relation: :hasFather
    target: Louis_XIV
  AddTriple (c9436291-5f5d-4be9-934c-8576b1a3e394)
 Call ID: c9436291-5f5d-4be9-934c-8576b1a3e394
  Args:
    relation: :hasAncestor
    source: Henri_d_Orleans
    target: Francoise_Marie_de_Bourbon
  AssignClass (3591409a-b22b-4788-8dc6-e5ecede59535)
 Call ID: 3591409a-b22b-4788-8dc6-e5ecede59535
  Args:
    type: :Man
    source: Louis_Philippe_I
  AssignClass (4a5198c3-9db8-4c38-81d1-748da9b74c46)
 Call ID: 4a5198c3-9db8-4c38-81d1-748da9b74c46
  Args:
    source: Louis_Philippe_I
    type: :Ancestor
  AddTriple (2d5aa32e-38ac-4b92-a0a7-263d88b4163d)
 Call ID: 2d5aa32e-38ac-4b92-a0a7-263d88b4163d
  Args:
    target: Louis_Philippe_I
    relation: :hasAncestor
    source: Henri_d_Orleans
  AssignClass (69b6c515-bedf-450b-bca7-9276c30c594e)
 Call ID: 69b6c515-bedf-450b-bca7-9276c30c594e
  Args:
    type: :Man
    source: Philippe_Duke_of_Orleans_maternal_uncle
  AssignClass (f7fe88cf-6c9b-452c-93fa-3bc0f2e97d64)
 Call ID: f7fe88cf-6c9b-452c-93fa-3bc0f2e97d64
  Args:
    source: Philippe_Duke_of_Orleans_maternal_uncle
    type: :Ancestor
  AssignClass (83883fd0-c69d-40fa-a49e-c1e7f20d5bdc)
 Call ID: 83883fd0-c69d-40fa-a49e-c1e7f20d5bdc
  Args:
    type: :Man
    source: Eudes_Duke_of_Angouleme
  AssignClass (5bd47560-0b7d-4823-8608-d7564935f93f)
 Call ID: 5bd47560-0b7d-4823-8608-d7564935f93f
  Args:
    type: :Person
    source: Eudes_Duke_of_Angouleme
  Finish (a9d48c67-deb9-4819-8415-a96101e78d30)
 Call ID: a9d48c67-deb9-4819-8415-a96101e78d30
  Args: